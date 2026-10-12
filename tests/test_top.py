from expense_tracker.commands import add, top
from tests.conftest import args, make_store


def _seed(store):
    add.handle(
        args(amount="12.50", category="groceries", date="2026-01-15", note="weekly shop"), store
    )
    add.handle(args(amount="40.00", category="transport", date="2026-01-16", note=""), store)
    add.handle(
        args(amount="4.20", category="food", date="2026-01-08", note="morning coffee"), store
    )
    add.handle(args(amount="100.00", category="rent", date="2026-01-01", note=""), store)


def test_top_default_limit_largest_first(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()  # discard output from seeding

    code = top.handle(args(limit=3), store)
    out = capsys.readouterr().out.splitlines()

    assert code == 0
    assert out == [
        "#4  2026-01-01     $100.00  rent",
        "#2  2026-01-16      $40.00  transport",
        "#1  2026-01-15      $12.50  groceries  (weekly shop)",
    ]


def test_top_respects_limit(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()

    code = top.handle(args(limit=2), store)
    out = capsys.readouterr().out.splitlines()

    assert code == 0
    assert [line.split()[0] for line in out] == ["#4", "#2"]


def test_top_limit_larger_than_count_shows_all(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()

    code = top.handle(args(limit=10), store)
    out = capsys.readouterr().out.splitlines()

    assert code == 0
    assert [line.split()[0] for line in out] == ["#4", "#2", "#1", "#3"]


def test_top_ties_keep_insertion_order(tmp_path, capsys):
    store = make_store(tmp_path)
    add.handle(args(amount="5.00", category="a", date="2026-01-01", note=""), store)
    add.handle(args(amount="5.00", category="b", date="2026-01-02", note=""), store)
    capsys.readouterr()

    top.handle(args(limit=3), store)
    out = capsys.readouterr().out.splitlines()

    assert [line.split()[0] for line in out] == ["#1", "#2"]


def test_top_empty(tmp_path, capsys):
    store = make_store(tmp_path)

    code = top.handle(args(limit=3), store)
    out = capsys.readouterr().out

    assert code == 0
    assert "No expenses found." in out


def test_top_rejects_non_positive_limit(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()

    code = top.handle(args(limit=0), store)
    out = capsys.readouterr().out

    assert code == 1
    assert "error: limit must be a positive integer, got 0" in out
