# pylint: disable=missing-docstring
import datetime
import re

from fava.core.fava_options import InsertEntryOption
from fava.core.fava_options import parse_options
from fava.util.date import FiscalYearEnd


def test_fava_options(load_doc):
    """
    2016-06-14 custom "fava-option" "default-file"
    2016-04-14 custom "fava-option" "show-closed-accounts" "true"
    2016-04-14 custom "fava-option" "journal-show" "transaction open"
    2016-04-14 custom "fava-option" "currency-column" "10"
    2016-04-14 custom "fava-option" "indent" "4"
    2016-04-14 custom "fava-option" "insert-entry" "Ausgaben:Test"
    2016-04-14 custom "fava-option" "invalid"
    2016-04-14 custom "fava-option" "locale" "en"
    2016-04-14 custom "fava-option" "locale" "invalid"
    2016-04-14 custom "fava-option" "collapse-pattern" "Account:Name"
    2016-04-14 custom "fava-option" "collapse-pattern" "(invalid"
    2016-04-14 custom "fava-option" "fiscal-year-end" "01-11"
    """

    entries, _, _ = load_doc
    options, errors = parse_options(entries)

    assert len(errors) == 3

    assert options["indent"] == 4
    assert options["insert-entry"] == [
        InsertEntryOption(
            datetime.date(2016, 4, 14),
            re.compile("Ausgaben:Test"),
            "<string>",
            7,
        )
    ]
    assert options["show-closed-accounts"]
    assert options["journal-show"] == ["transaction", "open"]
    assert options["currency-column"] == 10
    assert options["collapse-pattern"] == [re.compile("Account:Name")]
    assert options["fiscal-year-end"] == FiscalYearEnd(1, 11)
