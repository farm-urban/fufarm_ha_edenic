# Contribution guidelines

The scaffold for this repository has been generated from [ludeeus/integration_blueprint](https://github.com/ludeeus/integration_blueprint). Please refer to that repository and the Home Assistant [developer guidelines](https://developers.home-assistant.io/) for information on how to contribute and style guidelines.

# Edenic API
The Edenic API is documented at https://api-docs.edenic.io/.

To test the API, create a `secrets.yaml` file (with `org_key` and `api_key`keys):
```
curl "https://api.edenic.io/api/v1/device/$(sed -n 's/^org_key: "\(.*\)"$/\1/p' ./secrets.yaml)" --header "Authorization: $(sed -n 's/^api_key: "\(.*\)"$/\1/p' ./secrets.yaml)" | jq
```

# Testing
Tests are in `tests` and `tests_live`
Run standard tests with: `pytest`
Run live tests with : `pytest tests_live -p no:homeassistant` - this requires a `secrets.yaml` file (see abobve).