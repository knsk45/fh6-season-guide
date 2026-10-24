"""Fixed editorial repair diagnoses, never executable instructions from logs."""
import re

FIELDS = ('title','points','conditionHtml','howHtml','tuneHtml')
LOCALE_ERROR = re.compile(
    r'(?m)^(?:(?:Error|ValueError): )?English locale is missing '
    r'(title|points|conditionHtml|howHtml|tuneHtml) for '
    r'(activity_[0-9]{1,3}_[a-z0-9_]{1,64})\s*$')
FULL_LOCALE_ERROR = re.compile(
    r'(?m)^(?:(?:Error|ValueError): )?data/current-season\.json must contain '
    r'a complete English locale for every activity\s*$')


def locale_failure(logs):
    return bool(LOCALE_ERROR.search(logs) or FULL_LOCALE_ERROR.search(logs))


def locale_context(logs):
    return ['English field: '+field+'; activity: '+activity
            for field,activity in LOCALE_ERROR.findall(logs)][:10]


def validate_locale(state):
    locales=state.get('locales',{})
    locale=locales.get('en',{}) if isinstance(locales,dict) else {}
    if (not isinstance(locale,dict) or
            any(not isinstance(locale.get(k),str) or not locale[k].strip()
                for k in ('reportTitle','seasonDisplay')) or
            not isinstance(locale.get('activities'),dict)):
        raise ValueError('data/current-season.json must contain a complete English locale for every activity')
    for card in state['activities']:
        translation=locale['activities'].get(card['id'],{})
        for field in FIELDS:
            if not isinstance(translation,dict) or not isinstance(translation.get(field),str) or not translation[field].strip():
                raise ValueError('English locale is missing '+field+' for '+card['id'])
