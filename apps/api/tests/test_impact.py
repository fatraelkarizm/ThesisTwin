from datetime import UTC, datetime

from app.domain.brief import build_brief, render_text
from app.domain.diff import diff_elements
from app.domain.impact import change_impact
from app.domain.rules import Element
from app.services.config import ontology


def E(id_, type_, content):
    return Element(id_, type_, content, 1)


OLD = [
    E("p", "population", "Siswa kelas VIII SMP N 1."),
    E("m", "method", "Simple random sampling 30 siswa."),
    E("c", "claim", "Hasil berlaku untuk siswa kelas VIII SMP N 1."),
]
NEW = [
    E("p2", "population", "Seluruh siswa SMP negeri di Kota Bandung."),
    E("m2", "method", "Simple random sampling 30 siswa."),
    E("c2", "claim", "Hasil berlaku untuk siswa kelas VIII SMP N 1."),
]


def test_population_change_flags_sampling_and_generalisation():
    impacts = change_impact(diff_elements(OLD, NEW), NEW, ontology())
    by_type = {i.affected_type: i for i in impacts}
    assert {"method", "claim"} <= set(by_type)
    assert "sampling" in by_type["method"].check
    # metode & klaim tidak berubah sama sekali padahal populasi berubah -> belum diperbarui
    assert by_type["method"].stale and by_type["claim"].stale


def test_updated_dependent_is_not_stale():
    new = NEW[:1] + [E("m3", "method", "Cluster random sampling per kecamatan, 300 siswa."), NEW[2]]
    by_type = {i.affected_type: i for i in change_impact(diff_elements(OLD, new), new, ontology())}
    assert not by_type["method"].stale and by_type["claim"].stale


def test_no_changes_no_impacts():
    assert change_impact(diff_elements(OLD, OLD), OLD, ontology()) == []


def test_brief_text_lists_rechecks():
    d = diff_elements(OLD, NEW)
    b = build_brief(
        project_title="S",
        program="matematika",
        from_version=1,
        to_version=2,
        generated_at=datetime(2026, 11, 24, tzinfo=UTC),
        diff=d,
        comments=[],
        findings=[],
        previous_rules=set(),
        impacts=change_impact(d, NEW, ontology()),
        type_label=ontology().label,
    )
    text = render_text(b)
    assert "Perlu dicek ulang karena perubahan:" in text
    assert (
        "Populasi berubah → cek metode/desain" in text and "belum berubah sejak versi lalu" in text
    )
