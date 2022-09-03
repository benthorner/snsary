from snsary.utils.tracing import GapAlert, History, LivenessAlert, Sample


class TestGapAlert:
    def test_analyse(self, caplog):
        monitor = GapAlert(max_gaps=1)
        expected_log = "Alert: 2 gaps in last sample window"

        # first gap
        monitor.analyse(Sample.FAILURE)
        monitor.analyse(Sample.FAILURE)
        monitor.analyse(Sample.SUCCESS)
        assert expected_log not in caplog.text

        # second gap
        monitor.analyse(Sample.FAILURE)
        monitor.analyse(Sample.SUCCESS)
        assert expected_log in caplog.text
        caplog.clear()

        # first gap (after reset)
        monitor.analyse(Sample.FAILURE)
        monitor.analyse(Sample.SUCCESS)
        assert expected_log not in caplog.text

        # not a gap
        monitor.analyse(Sample.FAILURE)
        assert expected_log not in caplog.text


class TestLivenessAlert:
    def test_analyse(self, caplog):
        monitor = LivenessAlert(history=History(max_length=2))
        expected_log = "Alert: 2 failures in sample window"

        # first fail
        monitor.analyse(Sample.FAILURE)
        assert expected_log not in caplog.text

        # second fail
        monitor.analyse(Sample.FAILURE)
        assert expected_log in caplog.text
        caplog.clear()

        # first fail (after reset)
        monitor.analyse(Sample.FAILURE)
        assert expected_log not in caplog.text

        # not a fail
        monitor.analyse(Sample.SUCCESS)
        assert expected_log not in caplog.text
