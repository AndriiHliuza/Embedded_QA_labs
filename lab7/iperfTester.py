import parser


class TestSuite():
    def test_iperf3_client_connection(self, client):
        transfer_min_value = 1111111
        bitrate_min_value = 20

        transfer_criteria = lambda result: result['Transfer'] >= transfer_min_value
        bitrate_criteria = lambda result: result['Bitrate'] >= bitrate_min_value

        output, error = client

        if error:
            assert False, f"Error while connecting client: {error}"

        results = parser.parse(output)

        if not results:
            assert False, f"Incorrect client output"

        if not any(transfer_criteria(result) for result in results):
            assert False, f"Transfer criteria not met. All Transfer values < {transfer_min_value}"

        if not any(bitrate_criteria(result) for result in results):
            assert False, f"Bitrate criteria not met. All Bitrate values < {bitrate_min_value}"

        assert True
