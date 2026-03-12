import httpx
import json
import sys

def main():
    if len(sys.argv) != 2:
        print('Usage: py scripts/get_hue_app_key.py <bridge_ip>')
        sys.exit(1)

    bridge_ip = sys.argv[1].strip()

    url = f'https://{bridge_ip}/api'
    payload = {
        'devicetype': 'hue-loacal-api#desktop'
    }

    try:
        response = httpx.post(url, json=payload, timeout=10.0, verify=False)
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPError as exc:
        print(f'Request failed: {exc}')
        sys.exit(1)
    except ValueError:
        print('Invalid JSON response from Hue Bridge')
        sys.exit(1)

    print(json.dumps(data, indent=2))

    if isinstance(data, list) and data:
        item = data[0]

        if 'error' in item:
            error = item['error']
            print()
            print('Hue Bridge returned an error:')
            print(f'- type: {error.get('type')}')
            print(f'- description: {error.get('description')}')
            print()
            print('If the description says to press the link button, press the physical button on the Hue Bridge and run the script again.')

        if 'success' in item:
            success = item['success']
            username = success.get('username')

            print()
            print('HUE_APP_KEY obtained successfully:')
            print(f'HUE_APP_KEY={username}')


if __name__ == '__main__':
    main()
