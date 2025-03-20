from typing import TYPE_CHECKING, Any, Literal
from dataclasses import dataclass, field

from pypacks.resources.base_resource import BaseResource

if TYPE_CHECKING:
    from pypacks.pack import Pack

LanguageCode = Literal[
    "af_za", "ar_sa", "ast_es", "az_az", "ba_ru", "bar", "be_by", "be_latn", "bg_bg", "br_fr", "brb", "bs_ba", "ca_es", "cs_cz", "cy_gb", "da_dk",
    "de_at", "de_ch", "de_de", "el_gr", "en_au", "en_ca", "en_gb", "en_nz", "en_pt", "en_ud", "en_us", "enp", "enws", "eo_uy", "es_ar", "es_cl",
    "es_ec", "es_es", "es_mx", "es_uy", "es_ve", "esan", "et_ee", "eu_es", "fa_ir", "fi_fi", "fil_ph", "fo_fo", "fr_ca", "fr_fr", "fra_de", "fur_it",
    "fy_nl", "ga_ie", "gd_gb", "gl_es", "haw_us", "he_il", "hi_in", "hn_no", "hr_hr", "hu_hu", "hy_am", "id_id", "ig_ng", "io_en", "is_is", "isv",
    "it_it", "ja_jp", "jbo_en", "ka_ge", "kk_kz", "kn_in", "ko_kr", "ksh", "kw_gb", "la_la", "lb_lu", "li_li", "lmo", "lo_la", "lol_us", "lt_lt",
    "lv_lv", "lzh", "mk_mk", "mn_mn", "ms_my", "mt_mt", "nah", "nds_de", "nl_be", "nl_nl", "nn_no", "no_no", "oc_fr", "ovd", "pl_pl", "pt_br",
    "pt_pt", "qya_aa", "ro_ro", "rpr", "ru_ru", "ry_ua", "sah_sah", "se_no", "sk_sk", "sl_si", "so_so", "sq_al", "sr_cs", "sr_sp", "sv_se", "sxu",
    "szl", "ta_in", "th_th", "tl_ph", "tlh_aa", "tok", "tr_tr", "tt_ru", "tzo_mx", "uk_ua", "val_es", "vec_it", "vi_vn", "vp_vl", "yi_de", "yo_ng",
    "zh_cn", "zh_hk", "zh_tw", "zlm_arab",
]


language_groups: dict[str, list[LanguageCode]] = {
    "English": [
        "en_us", "en_gb", "en_au", "en_ca", "en_nz", "en_pt", "en_ud", "enp", "enws", "io_en"
    ],
    "Spanish": [
        "es_es", "es_mx", "es_ar", "es_cl", "es_ec", "es_uy", "es_ve", "esan"
    ],
    "Portuguese": [
        "pt_br", "pt_pt"
    ],
    "French": [
        "fr_fr", "fr_ca", "br_fr", "oc_fr"
    ],
    "German": [
        "de_de", "de_at", "de_ch", "nds_de"
    ],
    "Dutch": [
        "nl_nl", "nl_be", "fy_nl"
    ],
    "Italian": [
        "it_it", "vec_it", "fur_it", "lmo"
    ],
    "Chinese": [
        "zh_cn", "zh_hk", "zh_tw", "lzh"
    ],
    "Russian": [
        "ru_ru", "ba_ru", "tt_ru"
    ],
    "Ukrainian/Belarusian": [
        "uk_ua", "be_by", "be_latn", "ry_ua"
    ],
    "Scandinavian": [
        "da_dk", "sv_se", "no_no", "nn_no", "se_no"
    ],
    "Finnish/Estonian": [
        "fi_fi", "et_ee"
    ],
    "Slavic": [
        "pl_pl", "cs_cz", "sk_sk", "sl_si", "sr_cs", "sr_sp", "hr_hr", "mk_mk", "bg_bg", "szl"
    ],
    "Greek": [
        "el_gr"
    ],
    "Turkic": [
        "tr_tr", "az_az", "kk_kz", "sah_sah"
    ],
    "Arabic/Persian": [
        "ar_sa", "fa_ir", "zlm_arab"
    ],
    "Japanese": [
        "ja_jp"
    ],
    "Korean": [
        "ko_kr"
    ],
    "Indic": [
        "hi_in", "kn_in", "ta_in"
    ],
    "Celtic": [
        "ga_ie", "gd_gb", "kw_gb", "brb"
    ],
    "Esperanto": [
        "eo_uy"
    ],
    "Hebrew": [
        "he_il"
    ],
    "Miscellaneous": [
        "haw_us", "hy_am", "ig_ng", "is_is", "isv", "jbo_en", "ka_ge", "la_la", "lb_lu",
        "li_li", "lo_la", "lol_us", "lv_lv", "mn_mn", "ms_my", "mt_mt", "nah", "qya_aa",
        "rpr", "so_so", "sq_al", "sxu", "th_th", "tlh_aa", "tok", "tt_ru", "tzo_mx",
        "val_es", "vi_vn", "vp_vl", "yi_de", "yo_ng", "ovd"
    ]
}


@dataclass
class Translate:
    """Translate a string to a different language"""
    translation_code: str | dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        if isinstance(self.translation_code, dict):
            return self.translation_code | {"translate": self.translation_code["translate"]}  # If it's a dict, merge translation translation, so just return it
        return {
            "translate": self.translation_code
        }


@dataclass
class CustomLanguage(BaseResource):
    """Custom language, used for translations"""
    # https://minecraft.wiki/w/Resource_pack#Language
    language_code: LanguageCode  # e.g. en_us
    translations: dict[str, str]

    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="lang")

    def __post_init__(self) -> None:
        self.internal_name = self.language_code

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return self.translations

    @classmethod
    def from_dict(cls, language_code: LanguageCode, data: dict[str, str]) -> "CustomLanguage":  # type: ignore[override]
        return cls(language_code, data)

    def get_run_command(self, pack_namespace: str, translation_code: str) -> str:
        return f"tellraw @a {{\"translate\": \"{translation_code}\"}}"

    @staticmethod
    def propogate_to_all_similar_languages(pack: "Pack") -> None:
        """Propogate the translation to all similar languages, e.g. en_us to en_gb, en_au, etc."""
        # TODO: Even if the language exists, it might be missing keys, add those too!
        # en_us -> en_gb, en_au, en_ca, en_nz, en_ud, en_pt
        # es_es -> es_ar, es_cl, es_ec, es_mx, es_uy, es_ve
        # For each language group, find the missing languages and create a new language with the translations of the first instance of the language
        for _language_group_name, language_codes in language_groups.items():
            first_instance = [x for x in pack.custom_languages if x.language_code in language_codes]
            if not first_instance:  # We have none from that group, so we can't propogate
                continue
            currently_supported_language_codes = [language.language_code for language in pack.custom_languages]
            missing_languages: list[LanguageCode] = [language_code for language_code in language_codes if language_code not in currently_supported_language_codes]
            for missing_language in missing_languages:
                pack.custom_languages.append(CustomLanguage(missing_language, first_instance[0].translations))
                # rint("Added", missing_language, "to", _language_group_name)

    @staticmethod
    def combine_languages(pack: "Pack") -> None:
        """Combine all languages with one language_code into a single language file"""
        combined_languages: list["CustomLanguage"] = []
        all_existing_language_codes: set["LanguageCode"] = {language.language_code for language in pack.custom_languages}
        for language_code in all_existing_language_codes:
            combined_language_translations: dict[str, str] = {}
            for language in pack.custom_languages:
                if language.language_code == language_code:
                    combined_language_translations |= language.translations
            combined_languages.append(CustomLanguage(language_code, combined_language_translations))
        pack.custom_languages = combined_languages

    @classmethod
    def from_all_translation_keys(cls, language_mapping: dict[str, dict[LanguageCode, str]]) -> list["CustomLanguage"]:
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
        language_codes: set[LanguageCode] = {lang for translations in language_mapping.values() for lang in translations}
        # We need to reverse it, so rather then being grouped by translation_code, we need to group by language_code
        reversed_mapping: dict[LanguageCode, dict[str, str]] = {
            lang: {item: translations[lang] for item, translations in language_mapping.items() if lang in translations}
            for lang in language_codes
        }
        return [CustomLanguage(language_code, translations) for language_code, translations in reversed_mapping.items()]

    @classmethod
    def from_all_languages(cls, language_mapping: dict[LanguageCode, dict[str, str]]) -> list["CustomLanguage"]:
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
