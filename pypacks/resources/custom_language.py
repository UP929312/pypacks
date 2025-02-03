import os
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


# @dataclass
# class Translate:
#     """Translate a string to a language"""
#     translation_code: str

#     def to_dict(self, pack_namespace: str) -> dict[str, Any]:
#         return {
#             "translate": self.translation_code
#         }


@dataclass
class CustomLanguage:
    """Custom language, used for translations"""
    # https://minecraft.wiki/w/Resource_pack#Language
    language_code: LanguageCodes  # e.g. en_us
    translations: dict[str, str]

    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="lang")

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return self.translations
    
    def get_run_command(self, pack_namespace: str, translation_code: str) -> str:
        return f"tellraw @a [{{\"text\":\"{{\\\"translate\\\":\\\"{pack_namespace}.{self.language_code}.{translation_code}\\\"}}\"}}]"

    def create_resource_pack_files(self, pack: "Pack") -> None:
        # import os
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name, exist_ok=True)
        with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name/f"{self.language_code}.json", "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)


    def propogate_to_all_similar_languages(self, pack: "Pack") -> None:
        """Propogate the translation to all similar languages, e.g. en_us to en_gb, en_au, etc."""
        # TODO: Propogate to all similar languages
        # https://minecraft.wiki/w/Language
        # en_us -> en_gb, en_au, en_ca, en_nz, en_ud, en_pt
        # es_es -> es_ar, es_cl, es_ec, es_mx, es_uy, es_ve
        # fr_fr -> fr_ca, fra_de
        # de_de -> de_at, de_ch
        # pt_pt -> pt_br
        # ru_ru -> ry_ua
        # zh_cn -> zh_hk, zh_tw
        # sr_sp -> sr_cs
        raise NotImplementedError
        

    @classmethod
    def from_all_translation_keys(cls, language_mapping: dict[str, dict[LanguageCodes, str]]) -> list["CustomLanguage"]:
        """Used to be able to create multiple translations easily, e.g.
        CustomLanguage.from_all_translation_keys(
            {
                "item.minecraft.diamond", {
                    "en_us": "Diamond", "es_es": "Diamante", "en_gb": "Diamond", "fr_fr": "Diamant",
                },
                "item.minecraft.gold_ingot", {
                    "en_us": "Gold Ingot", "es_es": "Lingote de oro", "en_gb": "Gold Ingot", "fr_fr": "Lingot d'or",
            }
        )
        """
        # Get all language codes (e.g. en_us, en_gb, es_es, etc.)
        language_codes: set[LanguageCodes] = {lang for translations in language_mapping.values() for lang in translations}
        # We need to reverse it, so rather then being grouped by translation_code, we need to group by language
        reversed_mapping: dict[LanguageCodes, dict[str, str]] = {
            lang: {item: translations[lang] for item, translations in language_mapping.items() if lang in translations}
            for lang in language_codes
        }
        return [CustomLanguage(language_code, translations) for language_code, translations in reversed_mapping.items()]

    @classmethod
    def from_all_languages(cls, language_mapping: dict[LanguageCodes, dict[str, str]]) -> list["CustomLanguage"]:
        """Used to be able to create multiple translations easily, e.g.
        CustomLanguage.from_all_languages(
            "en_us": {
                "item.minecraft.diamond": "Diamond",
                "item.minecraft.gold_ingot": "Gold Ingot",
            },
            "es_es": {
                "item.minecraft.diamond": "Diamante",
                "item.minecraft.gold_ingot": "Lingote de oro",
            },
            "en_gb": {
                "item.minecraft.diamond": "Diamond",
                "item.minecraft.gold_ingot": "Gold Ingot",
            },
        )
        """
        return [CustomLanguage(language_code, translations) for language_code, translations in language_mapping.items()]
