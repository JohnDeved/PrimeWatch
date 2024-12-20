# PrimeWatch

## Project Description

PrimeWatch is a Python script that monitors the Amazon Prime Gaming website for new free game offers and sends notifications to a Discord channel using a webhook. The script extracts the necessary information from the Amazon Prime Gaming website and sends it to the Discord channel in the form of embeds.

### Installation

1. Clone the repository:

```bash
git clone https://github.com/JohnDeved/PrimeWatch.git
cd PrimeWatch
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Create a `config.ini` file with your Discord webhook URL:

```ini
[webhook]
url = YOUR_DISCORD_WEBHOOK_URL
```

4. Run the script:

```bash
python watch.py
```