import json

def shapeless_recipe_template(ingredients: list[str | list[str]], result: str, amount: int = 1) -> str:
    return json.dumps({
        "type": "minecraft:crafting_shapeless",
        "ingredients": ingredients,
        "result": {
            "id": result,
            "count": amount,
        }
    }, indent=4)


def shaped_recipe_template(pattern: str | list[str], keys: dict[str, str | list[str]], result: str, amount: int = 1) -> str:
    return json.dumps({
        "type": "minecraft:crafting_shaped",
        "pattern": pattern,
        "key": keys,
        "result": {
            "id": result,
            "count": amount,
        },
        "show_notification": True,
    }, indent=4)


def furnace_recipe_template(ingredient: str, result: str, experience: int | None = 1, cooking_time_ticks: int = 200) -> str:
    return json.dumps({
        "type": "minecraft:smelting",
        "ingredient": ingredient,
        "result": {
            "id": result,
        },
        "experience": experience,
        "cookingtime": cooking_time_ticks
    }, indent=4)


def smoker_recipe_template(ingredient: str, result: str, experience: int | None = 1, cooking_time_ticks: int = 200) -> str:
    return json.dumps({
        "type": "minecraft:smoking",
        "ingredient": ingredient,
        "result": {
            "id": result,
        },
        "experience": experience,
        "cookingtime": cooking_time_ticks
    }, indent=4)