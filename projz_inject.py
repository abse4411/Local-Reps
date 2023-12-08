# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>, modified by https://github.com/abse4411
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import renpy.translation
from renpy.translation.generation import *
import json
import collections

def item_of(
    identifier=None,
    language=None,
    what=None,
    new_text=None,
    who=None,
    filename=None,
    linenumber=None,
):
    return {
        'identifier':identifier,
        'language':language,
        'what':what,
        'new_text':new_text,
        'who': who,
        'filename':filename,
        'linenumber':linenumber,
    }

def get_text(t):
    if t is not None:
        for i in t.block:
            if isinstance(i, renpy.ast.Say):
                return i.what

    return None

def count_missing(language, min_priority, max_priority, common_only):
    """
    Prints a count of missing translations for `language`.
    """

    translator = renpy.game.script.translator

    missing_translates = 0

    missing_items = []
    for filename in translate_list_files():
        for _, t in translator.file_translates[filename]:
            if (t.identifier, language) not in translator.language_translates:
                missing_translates += 1
                for i, n in enumerate(t.block):
                    missing_items.append(item_of(
                        identifier=t.identifier.replace('.', '_'),
                        language=language,
                        what=n.what,
                        who=n.who,
                        filename=t.filename,
                        linenumber=t.linenumber,
                    ))

    missing_strings = 0

    stl = renpy.game.script.translator.strings[language] # @UndefinedVariable

    strings = renpy.translation.scanstrings.scan(min_priority, max_priority, common_only)

    missing_strings_items = []
    for s in strings:

        tlfn = translation_filename(s)

        if tlfn is None:
            continue

        if s.text in stl.translations:
            continue

        missing_strings += 1
        missing_strings_items.append(item_of(
            identifier=quote_unicode(s.text),
            language=language,
            what=quote_unicode(s.text),
            filename=elide_filename(s.filename),
            linenumber=s.line,
        ))

    message = "{}: {} missing dialogue translations, {} missing string translations.".format(
            language,
            missing_translates,
            missing_strings
            ),
    return message, {
        'missing_items':missing_items,
        'missing_strings':missing_strings_items,
    }

def get_translation(filename, language, all_strings):

    fn, common = shorten_filename(filename)

    # The common directory should not have dialogue in it.
    if common:
        return []

    raw_language = language
    if language == "None":
        language = None

    translator = renpy.game.script.translator

    item_list = []
    for label, t in translator.file_translates[filename]:
        identifier = t.identifier
        if not all_strings:
            if (t.identifier, language) in translator.language_translates:
                continue

            if hasattr(t, "alternate"):
                identifier = t.alternate
                if (t.alternate, language) in translator.language_translates:
                    continue

        for i, n in enumerate(t.block):
            item_list.append(item_of(
                identifier=identifier.replace('.', '_'),
                language=raw_language,
                what=n.what,
                new_text=get_text(translator.language_translates.get((t.identifier, language), None)),
                who=n.who,
                filename=t.filename,
                linenumber=t.linenumber,
            ))
    return item_list

def get_string_translation(language, filter, min_priority, max_priority, common_only, all_strings):
    """
    get strings to a list
    """
    if language == "None":
        stl = renpy.game.script.translator.strings[None] # @UndefinedVariable
    else:
        stl = renpy.game.script.translator.strings[language] # @UndefinedVariable

    # If this function changes, count_missing may also need to
    # change.

    strings = renpy.translation.scanstrings.scan(min_priority, max_priority, common_only)

    stringfiles = collections.defaultdict(list)

    for s in strings:

        tlfn = translation_filename(s)

        if tlfn is None:
            continue

        if not all_strings:
            # Already seen.
            if s.text in stl.translations:
                continue

        if language == "None" and tlfn == "common.rpy":
            tlfn = "common.rpym"

        stringfiles[tlfn].append(s)

    item_list = []
    for tlfn, sl in stringfiles.items():

        for s in sl:
            text = filter(s.text)

            item_list.append(item_of(
                identifier=quote_unicode(s.text),
                language=language,
                what=quote_unicode(text),
                new_text=stl.translations.get(s.text, None),
                filename=elide_filename(s.filename),
                linenumber=s.line,
            ))
    return item_list

def projz_inject_command():
    """
    The injection command. When called from the command line, this
    injects our code for extracting translations.
    """

    ap = renpy.arguments.ArgumentParser(description="Injection for extracting translations.")
    ap.add_argument("uuid", help="The uuid to identify the json file generated by our code")
    ap.add_argument("--test-only", help="Test this command with doing anything", dest="test_only", action="store_true")
    ap.add_argument("--all-strings", help="Extract all strings, including translated ones",
                    dest="all_strings", action="store_true")
    ap.add_argument("--language", help="The language to generate translations for.", default="None")
    ap.add_argument("--rot13", help="Apply rot13 while generating translations.", dest="rot13", action="store_true")
    ap.add_argument("--piglatin", help="Apply pig latin while generating translations.", dest="piglatin", action="store_true")
    ap.add_argument("--count", help="Instead of generating files, print a count of missing translations.", dest="count", action="store_true")
    ap.add_argument("--min-priority", help="Translate strings with more than this priority.", dest="min_priority", default=0, type=int)
    ap.add_argument("--max-priority", help="Translate strings with more than this priority.", dest="max_priority", default=0, type=int)
    ap.add_argument("--strings-only", help="Only translate strings (not dialogue).", dest="strings_only", default=False, action="store_true")
    ap.add_argument("--common-only", help="Only translate string from the common code.", dest="common_only", default=False, action="store_true")

    args = ap.parse_args()

    def write_json(items=None, message=None, ok=None):
        with open('translation.json', 'w', encoding = 'utf-8') as f:
            f.write(json.dumps({
                'uuid': args.uuid,
                'args': str(args),
                'timestamp': time.time(),
                'items': items,
                'message': message,
                'ok': ok
            },ensure_ascii=False, indent=2, encoding= 'utf-8'))


    if args.test_only:
        write_json([], '', True)
        return False

    if renpy.config.translate_launcher:
        max_priority = args.max_priority or 499
    else:
        max_priority = args.max_priority or 299

    if args.count:
        msg, res = count_missing(args.language, args.min_priority, max_priority, args.common_only)
        write_json(res, msg, True)
        for k,v in res.items():
            print k,len(v)
        return False

    if args.rot13:
        filter = rot13_filter # @ReservedAssignment
    elif args.piglatin:
        filter = piglatin_filter # @ReservedAssignment
    else:
        filter = null_filter # @ReservedAssignment

    try:
        dialogue_items = []
        if not args.strings_only:
            for filename in translate_list_files():
                dialogue_items += get_translation(filename, args.language, args.all_strings)
        items = get_string_translation(args.language, filter, args.min_priority, max_priority,
                               args.common_only, args.all_strings)
        all_items = items + dialogue_items

        write_json(all_items, '{}: {} dialogue translations found, {} string translations found'.format(
            args.language,
            len(dialogue_items),
            len(items),
        ), True)
    except Exception as e:
        write_json([], 'An error occurred while extracting translations: ' + str(e), False)
        raise e
    return False


renpy.arguments.register_command("projz_inject_command", projz_inject_command)
