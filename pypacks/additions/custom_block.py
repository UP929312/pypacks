from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pypacks.resources.custom_advancement import Criteria, CustomAdvancement
from pypacks.resources.custom_model import FacePaths, AsymmetricCubeModel, SymmetricCubeModel, SlabModel
from pypacks.resources.custom_loot_tables.custom_loot_table import CustomLootTable, SingleItemPool
from pypacks.resources.custom_mcfunction import MCFunction
from pypacks.additions.raycasting import BlockRaycast

if TYPE_CHECKING:
    from typing import Literal
    from pypacks.pack import Pack
    from pypacks.additions.constants import Slabs
    from pypacks.resources.custom_predicate import Predicate
    from pypacks.resources.custom_item import CustomItem


@dataclass
class CustomBlock:
    """Adds a custom block, for the texture, pass in a single 16x16 texture path, or a FacePaths object, which allows multiple paths to be
    passed in (e.g. rotatable logs). Setting drops to "self" will make the block drop itself when broken,
    and setting it to None will make it drop nothing."""
    internal_name: str
    base_block: str
    block_texture: "str | FacePaths" = field(repr=False)
    drops: "Literal['self'] | CustomItem | CustomLootTable | str | None" = field(repr=False, default="self")
    silk_touch_drops: "Literal['self'] | CustomItem | CustomLootTable | str | None" = "self"
    # fortune_drops: "Literal['self'] | CustomItem | CustomLootTable | str | None" = "self"
    # on_right_click: str | None = None  # For things like inventories, custom furnaces, etc?

    block_item: "CustomItem | None" = field(init=False, repr=False, hash=False, default=None)  # Used by datapack to create the custom icons

    def __post_init__(self) -> None:
        if isinstance(self.block_texture, str):
            self.block_texture = FacePaths(self.block_texture, None, None, None, None, None)

        if self.block_texture.block_type == "symmetric_cube":
            self.model_object: SymmetricCubeModel | AsymmetricCubeModel = SymmetricCubeModel(self.internal_name, self.block_texture.front)
        elif self.block_texture.block_type == "asymmetric_cube":
            self.model_object = AsymmetricCubeModel(self.internal_name, self.block_texture)

    @staticmethod
    def create_silk_touch_predicate() -> "Predicate":
        from pypacks.resources.predicate.predicates import EntityPropertiesPredicate
        from pypacks.resources.predicate.predicate_conditions import EntityCondition
        from pypacks.resources.predicate.predicate_conditions import ItemCondition
        from pypacks.resources.predicate.data_component_predicate import EnchantmentComponentPredicate
        return EntityPropertiesPredicate(
            "silk_touch_check",
            "this",
            predicate=EntityCondition(
                equipment={"mainhand": ItemCondition(predicates=[EnchantmentComponentPredicate(enchantments=["minecraft:silk_touch"])])}
            ),
        )

    def set_or_create_loot_table(self) -> None:
        """Takes a CustomItem, item type, CustomLootTable, or None, and sets the loot_table attribute to a CustomLootTable object."""
        from pypacks.resources.custom_item import CustomItem
        self.regular_loot_table = None
        if self.drops == "self":
            if self.block_item is not None:
                self.regular_loot_table = CustomLootTable(f"{self.internal_name}_block_regular_drop_loot_table", pools=[SingleItemPool(self.block_item)])
            else:
                raise ValueError("If drops is set to 'self', then block_item must be set.")
        elif isinstance(self.drops, (CustomItem, str)):
            self.regular_loot_table = CustomLootTable(f"{self.internal_name}_block_regular_drop_loot_table", pools=[SingleItemPool(self.drops)])
        elif isinstance(self.drops, CustomLootTable):
            self.regular_loot_table = self.drops

        # TODO: DUPLICATED, CLEANUP SOON
        self.silk_touch_loot_table = None
        if self.silk_touch_drops == "self":
            if self.block_item is not None:
                self.silk_touch_loot_table = CustomLootTable(f"{self.internal_name}_block_silk_touch_drop_loot_table", pools=[SingleItemPool(self.block_item)])
            else:
                raise ValueError("If silk_touch_loot_table is set to 'self', then block_item must be set.")
        elif isinstance(self.silk_touch_drops, (CustomItem, str)):
            self.silk_touch_loot_table = CustomLootTable(f"{self.internal_name}_block_silk_touch__drop_loot_table", pools=[SingleItemPool(self.silk_touch_drops)])
        elif isinstance(self.silk_touch_drops, CustomLootTable):
            self.silk_touch_loot_table = self.silk_touch_drops

    @classmethod
    def from_item(
        cls, item: "CustomItem", block_texture: "str | FacePaths | None" = None,
        regular_drops: "Literal['self'] | CustomItem | CustomLootTable | None" = "self",
        silk_touch_drops: "Literal['self'] | CustomItem | CustomLootTable | None" = "self",
    ) -> "CustomBlock":
        """Used to create a new custom block."""
        assert item.custom_name is not None and item.texture_path is not None
        item.is_block = True
        class_ = cls(item.internal_name, item.base_item, block_texture or item.texture_path, drops=regular_drops, silk_touch_drops=silk_touch_drops)
        class_.block_item = item
        class_.block_item.custom_data[f"custom_right_click_for_{class_.internal_name}"] = True
        class_.set_or_create_loot_table()
        return class_

    def create_advancement(self, pack_namespace: str) -> "CustomAdvancement":
        """Required to detect when the custom block is placed."""
        condition = {
            "location": [
                {
                    "condition": "minecraft:match_tool",
                    "predicate": {
                        "predicates": {
                            "minecraft:custom_data": {f"custom_right_click_for_{self.internal_name}": True},
                        }
                    }
                }
            ]
        }
        criteria = Criteria(f"placed_{self.internal_name}", "minecraft:placed_block", conditions=condition)
        rewarded_function = f"{pack_namespace}:custom_blocks/revoke_and_run/revoke_and_run_{self.internal_name}"
        advancement = CustomAdvancement(f"placed_{self.internal_name}", criteria=[criteria], rewarded_function=rewarded_function, hidden=True)
        return advancement

    def generate_detect_rotation_function(self) -> "MCFunction":
        # Detect and store player rotation (when needed)
        return MCFunction("detect_rotation", [
            "execute store result score rotation player_yaw run data get entity @s Rotation[0] 1",
            "execute if score rotation player_yaw matches -45..45 run scoreboard players set rotation_group player_yaw 1",
            "execute if score rotation player_yaw matches 45..135 run scoreboard players set rotation_group player_yaw 2",
            "execute if score rotation player_yaw matches 135..180 run scoreboard players set rotation_group player_yaw 3",
            "execute if score rotation player_yaw matches -180..-135 run scoreboard players set rotation_group player_yaw 3",
            "execute if score rotation player_yaw matches -135..-45 run scoreboard players set rotation_group player_yaw 4",

            "execute store result score rotation player_pitch run data get entity @s Rotation[1] 1",
            "execute if score rotation player_pitch matches -90..-45 run scoreboard players set rotation_group player_pitch 1",  # Up
            "execute if score rotation player_pitch matches -45..45 run scoreboard players set rotation_group player_pitch 2",  # Flat
            "execute if score rotation player_pitch matches 45..90 run scoreboard players set rotation_group player_pitch 3",  # Down
        ], ["custom_blocks"])

    def generate_place_function(self, pack_namespace: str) -> "MCFunction":
        execute_as_item_display = self.generate_functions(pack_namespace)[0]
        return MCFunction(f"place_{self.internal_name}", [
            f"say Placed {self.internal_name}!",
            f"setblock ~ ~ ~ {self.base_block}",
            f"execute align xyz positioned ~.5 ~.5 ~.5 summon item_display run {execute_as_item_display.get_run_command(pack_namespace)}",
            ],
            ["custom_blocks", "on_place"],
        )

    def generate_functions(self, pack_namespace: str) -> tuple["MCFunction", ...]:
        """Generates the spawn function, and destroy"""
        assert isinstance(self.block_texture, FacePaths)  # Overridden in __post_init__
        # These are in reverse order (pretty much), so we can reference them in the next function.
        # ============================================================================================================
        # Has to be secondary so we have @s set correctly.
        execute_as_item_display = MCFunction(f"execute_on_item_display_{self.internal_name}", [
            # Give two tags:
            f"tag @s add {pack_namespace}.custom_block",
            f"tag @s add {pack_namespace}.custom_block.{self.internal_name}",

            # Make it _slightly_ bigger than the block, so it hides the original (only a tiny bit bigger), to stop z-fighting too.
            "data modify entity @s transformation.scale set value [1.002f, 1.002f, 1.002f]",  # Even slabs and stairs need the model at this scale
            "data modify entity @s brightness set value {block: 15, sky: 15}",

            # For item displays, container.0 is just the item it is displaying.
            f"item replace entity @s container.0 with minecraft:sponge[minecraft:item_model='{pack_namespace}:{self.internal_name}']",

            # ============================================================================================================
            # ROTATION:
            # Player horizontal rotation (yaw) is -180 -> 180, with -180/180 (they're the same) being directly north
            # North = 135 -> 180 & -180 -> -135  |  East = -135 -> -45  |  South = -45 -> 45  |  West = 45 -> 135
            *([
                f"execute if score rotation_group player_yaw matches {i} " +
                f"run execute at @s run rotate @s {(i+1)*90} 0"
                for i in [1, 2, 3, 4]
            ] if self.block_texture.horizontally_rotatable else []),

            # This does the same, but for pitch, which is in the -90 -> 90 range (-90 = looking up, 90 = looking down).
            *([
                f"execute if score rotation_group player_pitch matches {i} run execute at @s run rotate @s ~ {angle}"
                for i, angle in zip([1, 2, 3], [90, 0, -90])
            ] if self.block_texture.vertically_rotatable else []),

            ], ["custom_blocks", "execute_on_item_display"],
        )
        # Spawn the item display, then call the setup on it directly.
        spawn_item_display = MCFunction(f"setup_item_display_{self.internal_name}", [
            f"execute align xyz positioned ~.5 ~.5002 ~.5 summon item_display at @s run {execute_as_item_display.get_run_command(pack_namespace)}",
            ],
            ["custom_blocks", "setup_item_display"],
        )
        # ============================================================================================================
        deploy_raycast_function = BlockRaycast(
            self.internal_name,
            on_block_hit_command=spawn_item_display.get_run_command(pack_namespace),
            no_blocks_hit_command="say Raycasting failed!",
            blocks_to_detect=self.base_block,
            if_or_unless="if",
        ).create_deploy_function(pack_namespace)
        # ============================================================================================================
        revoke_and_run_mcfunction = MCFunction(f"revoke_and_run_{self.internal_name}", [
                f"advancement revoke @s only {pack_namespace}:placed_{self.internal_name}",
                self.generate_detect_rotation_function().get_run_command(pack_namespace),
                deploy_raycast_function.get_run_command(pack_namespace),
            ],
            ["custom_blocks", "revoke_and_run"],
        )
        # ============================================================================================================
        silk_touch_predicate = self.create_silk_touch_predicate().get_reference(pack_namespace)
        regular_loot_table = self.regular_loot_table.get_spawn_command(pack_namespace) if self.regular_loot_table is not None else None
        silk_touch_loot_table = self.silk_touch_loot_table.get_spawn_command(pack_namespace) if self.silk_touch_loot_table is not None else None
        commands = [
            "execute as @p if entity @p[gamemode=creative] run return fail",
            # Case 1: No silk touch, regular loot (return regular loot), e.g. dirt drops dirt without silk touch
            f"execute as @p unless predicate {silk_touch_predicate} run {regular_loot_table}" if self.regular_loot_table is not None else "# Doesn't drop non-silk touch loot.",
            # Case 2: No silk touch, no regular loot (return nothing)  e.g. glass_block drops nothing without silk touch
            # Case 3: Silk touch, silk touch loot (return silk touch loot)  e.g. glass_block drops glass_block with silk touch
            f"execute as @p if predicate {silk_touch_predicate} run {silk_touch_loot_table}" if self.silk_touch_loot_table is not None else "# Doesn't drop purely silk touch loot.",
            # Case 4: Silk touch, regular loot, no silk touch (return regular loot)  # e.g. cobblestone drops cobblestone with silk touch
            f"execute as @p if predicate {silk_touch_predicate} run {regular_loot_table}" if self.regular_loot_table is not None and self.silk_touch_loot_table is None else "# N/A",
            # Case 5: Silk touch, no regular loot, no silk touch (return nothing)  # e.g. monster spawner drops nothing, even with silk touch
        ]
        spawn_loot_function = MCFunction(f"spawn_loot_{self.internal_name}", commands, sub_directories=["custom_blocks", "spawn_loot"])  # type: ignore[arg-type]
        # ======
        on_destroy_no_silk_touch_function = MCFunction(
            f"on_destroy_no_silk_touch_{self.internal_name}", [
                # @s is the item display itself, ~ ~ ~ is the center of the block
                "kill @e[type=experience_orb, distance=..0.5]",  # Kill all xp orbs dropped
                "kill @e[type=item, distance=..0.5]",  # Kill all naturally dropped items
                # "kill @e[type=interaction, distance=..0.1]",  # Kill all interaction entities (if any)
                spawn_loot_function.get_run_command(pack_namespace),  # Spawn the loot
                "kill @s"  # Kill the item display
            ],
            ["custom_blocks", "on_destroy"],
        )
        # ============================================================================================================
        return execute_as_item_display, spawn_item_display, deploy_raycast_function, revoke_and_run_mcfunction, spawn_loot_function, on_destroy_no_silk_touch_function

    @staticmethod
    def on_tick_function(pack: "Pack") -> "MCFunction":
        """Runs every tick, but once per pack, not per block."""
        return MCFunction("all_blocks_tick", [
            # Kill all xp orbs and items, spawn the loot, then kill the item display itself.
            *[f"execute as @e[type=item_display, tag={pack.namespace}.custom_block.{custom_block.internal_name}] at @s if block ~ ~ ~ minecraft:air run function {pack.namespace}:custom_blocks/on_destroy/on_destroy_no_silk_touch_{custom_block.internal_name}"
              for custom_block in pack.custom_blocks],
        ], ["custom_blocks"])

    def create_slab(self, slab_block: "Slabs") -> "CustomBlock":
        """Adds a slab version of the block."""
        # TODO: Here
        # raise NotImplementedError
        assert isinstance(self.model_object, SymmetricCubeModel), "Slabs can only be added to symmetric cube blocks."
        assert self.block_item is not None, "Slabs can only be added to blocks with a block item."
        # =========================
        from pypacks.additions.text import Text
        from pypacks.resources.custom_item import CustomItem
        slab_model = SlabModel(f"{self.internal_name}_slab", self.model_object.texture_path)
        slab_item = CustomItem(
            f"{self.internal_name}_slab", base_item=f"minecraft:{slab_block}", custom_name=Text.from_input(self.block_item.custom_name or "Unknown").text+" Slab",
            lore=self.block_item.lore, custom_data={f"custom_right_click_for_{self.internal_name}_slab": True},
            components=self.block_item.components, item_model=slab_model,  # type: ignore[arg-type]
            ref_book_config=self.block_item.ref_book_config,
        )
        slab_item.texture_path = self.model_object.texture_path  # type: ignore[assignment]
        slab_item.is_block = True
        # =========================
        new_slab_block = CustomBlock(
            f"{self.internal_name}_slab", base_block=f"minecraft:{slab_block}", block_texture=self.block_texture, drops=slab_item
        )
        new_slab_block.block_item = slab_item
        new_slab_block.model_object = slab_model  # type: ignore[assignment]  # We have to do this or the regular block that gets created will override things
        new_slab_block.set_or_create_loot_table()
        return new_slab_block

    def create_resource_pack_files(self, pack: "Pack") -> None:
        self.model_object.create_resource_pack_files(pack)
