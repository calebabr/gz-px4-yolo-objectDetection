from types import SimpleNamespace

import pytest

from image_processing import behavior_logic as logic


def det(name='person', conf=0.9, area=1000.0, width=20.0, height=50.0, x=320.0, y=240.0):
    return SimpleNamespace(class_name=name, confidence=conf, pixel_area=area, width=width, height=height,
                           x_center=x, y_center=y)


# ---- R-4: process every frame by default, every n-th when asked ----

def test_every_frame_is_processed_when_n_is_one():
    assert all(logic.should_process(frame, 1) for frame in range(1, 30))


def test_every_nth_frame_when_n_is_five():
    processed = [frame for frame in range(1, 21) if logic.should_process(frame, 5)]
    assert processed == [5, 10, 15, 20]


@pytest.mark.parametrize('bad', [0, -3])
def test_invalid_n_falls_back_to_every_frame(bad):
    assert logic.should_process(7, bad)


# ---- scoring ----

def test_valid_detections_drops_empty_class_zero_confidence_and_zero_area():
    good = det()
    dets = [good, det(name=''), det(conf=0.0), det(area=0.0), det(conf=-1.0)]
    assert logic.valid_detections(dets) == [good]


def test_score_detections_with_nothing_valid():
    assert logic.score_detections([det(name='')]) == ([], [], None)
    assert logic.score_detections([]) == ([], [], None)


def test_the_larger_more_confident_detection_wins():
    small = det(conf=0.5, area=100.0)
    big = det(conf=0.9, area=1000.0)
    valid, scores, best = logic.score_detections([small, big])
    assert valid == [small, big]
    assert best == 1 and scores[1] > scores[0]


def test_scores_keep_the_input_order_and_best_is_the_maximum():
    dets = [det(conf=0.9, area=1000.0), det(conf=0.3, area=100.0), det(conf=0.6, area=700.0)]
    valid, scores, best = logic.score_detections(dets)
    assert len(scores) == 3
    assert scores[best] == max(scores)
    assert best == 0


def test_single_detection_scores_area_term_as_one():
    _, scores, best = logic.score_detections([det(conf=0.67, area=500.0)])
    # sigmoid(0.67 - 0.67) = 0.5 -> 0.5 * 0.5 + 0.5 * ~1.0
    assert best == 0
    assert scores[0] == pytest.approx(0.75, abs=1e-3)


def test_sigmoid_reference_values():
    assert logic.sigmoid(0.5, 5.0, 0.5) == pytest.approx(0.5)
    assert logic.sigmoid(1.0, 15.0, 0.67) > 0.99
    assert logic.sigmoid(0.0, 15.0, 0.67) < 0.001


# ---- R-3: features describe the CHOSEN detection ----

def test_features_use_the_main_detection_and_best_score():
    main = det(conf=0.9, area=1000.0, width=20.0, height=50.0)
    features = logic.build_features(main, 0.8)
    assert features == [0.9, 1000.0, 0.8, 20.0, 50.0, pytest.approx(0.4)]


def test_regression_r3_features_follow_main_not_the_last_detection():
    """The old code read `det`/`score`, the leftovers of the last loop iteration, so the features described the last
    detection instead of the chosen one."""
    best = det(conf=0.95, area=2000.0, width=40.0, height=80.0)
    last = det(conf=0.30, area=100.0, width=10.0, height=10.0)  # last in the list, but not the best
    valid, scores, best_index = logic.score_detections([best, last])
    main = valid[best_index]
    features = logic.build_features(main, scores[best_index])
    assert main is best
    assert features[0] == 0.95 and features[1] == 2000.0, 'confidence/area must come from the chosen detection'
    assert features[2] == scores[0], 'the score must be the best score, not the last detection\'s score'
    assert features[2] != scores[1]


def test_aspect_ratio_is_zero_for_a_flat_box_instead_of_dividing_by_zero():
    assert logic.build_features(det(width=10.0, height=0.0), 0.5)[5] == 0


# ---- image size unknown until the first frame arrives ----

def test_centre_offset_is_none_until_the_image_size_is_known():
    assert logic.normalised_centre_offset(det(), None, None) is None
    assert logic.normalised_centre_offset(det(), 0, 480) is None


def test_centre_offset_is_normalised_to_minus_one_to_one():
    assert logic.normalised_centre_offset(det(x=320.0, y=240.0), 640, 480) == (0.0, 0.0)
    assert logic.normalised_centre_offset(det(x=640.0, y=0.0), 640, 480) == (1.0, -1.0)
    assert logic.normalised_centre_offset(det(x=0.0, y=480.0), 640, 480) == (-1.0, 1.0)
