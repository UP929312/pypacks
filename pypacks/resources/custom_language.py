import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from pypacks.pack import Pack

LanguageCodes = Literal[
    "af_za", "ar_sa", "ast_es", "az_az", "ba_ru", "bar", "be_by", "be_latn", "bg_bg", "br_fr", "brb", "bs_ba", "ca_es", "cs_cz", "cy_gb", "da_dk",
    "de_at", "de_ch", "de_de", "el_gr", "en_au", "en_ca", "en_gb", "en_nz", "en_pt", "en_ud", "en_us", "enp", "enws", "eo_uy", "es_ar", "es_cl",
    "es_ec", "es_es", "es_mx", "es_uy", "es_ve", "esan", "et_ee", "eu_es", "fa_ir", "fi_fi", "fil_ph", "fo_fo", "fr_ca", "fr_fr", "fra_de", "fur_it",
    "fy_nl", "ga_ie", "gd_gb", "gl_es", "haw_us", "he_il", "hi_in", "hn_no", "hr_hr", "hu_hu", "hy_am", "id_id", "ig_ng", "io_en", "is_is", "isv",
    "it_it", "ja_jp", "jbo_en", "ka_ge", "kk_kz", "kn_in", "ko_kr", "ksh", "kw_gb", "la_la", "lb_lu", "li_li", "lmo", "lo_la", "lol_us", "lt_lt",
    "lv_lv", "lzh", "mk_mk", "mn_mn", "ms_my", "mt_mt", "nah", "nds_de", "nl_be", "nl_nl", "nn_no", "no_no", "oc_fr", "ovd", "pl_pl", "pt_br",
    "pt_pt", "qya_aa", "ro_ro", "rpr", "ru_ru", "ry_ua", "sah_sah", "se_no", "sk_sk", "sl_si", "so_so", "sq_al", "sr_cs", "sr_sp", "sv_se", "sxu",
    "szl", "ta_in", "th_th", "tl_ph", "tlh_aa", "tok", "tr_tr", "tt_ru", "tzo_mx", "uk_ua", "val_es", "vec_it", "vi_vn", "vp_vl", "yi_de", "yo_ng",
    "zh_cn", "zh_hk", "zh_tw", "zlm_arab",
]  # TODO: Allow to batch for languages, e.g. all the English speaking ones, all Spanish, etc.


@dataclass
class Translate:
    """Translate a string to a language"""
    translation_code: str

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "translate": self.translation_code
        }


@dataclass
class CustomLanguage:
    """Custom language, used for translations"""
    # https://minecraft.wiki/w/Resource_pack#Language
    language_code: LanguageCodes  # e.g. en_us
    translations: dict[str, str]

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="lang")

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return self.translations
    
    def get_run_command(self, pack_namespace: str, phrase: str) -> str:
        return f"tellraw @a [{{\"text\":\"{{\\\"translate\\\":\\\"{pack_namespace}.{self.language_code}.{phrase}\\\"}}\"}}]"

    def create_datapack_files(self, pack: "Pack") -> None:
        # import os
        # os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name, exist_ok=True)
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/f"{self.language_code}.json", "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)


# TODO: Make this work with regular packs, not just manually
# a = CustomLanguage("en_us", {"item.minecraft.diamond": "Diamond"})
# from pypacks.pack import Pack
# a.create_datapack_files(Pack("PyPacks Testing", "", "pypacks_testing", world_name="PyPacksWorld"))
