# Facebook Activity Tracker

This tool will let you track your facebook friends activity habits and generate nice statistics from it. 

Warning: This tool is only Python3 compatibible!

## Getting Started

You will need to install a couple of additional libraries:

```
pip install sqlite3 jinja2 fbchat pyaml
```

## Running 

You can either set the parameters in config.yaml file, or pass it from the CLI. Example of the second way:

```
python fb-activity-tracker.py --env=dev --user=your_fb_email --password=your_fb_password 
``` 

This command will start logging activity into updates.db file.

# Generating reports

This is simple, yet powerful tool. Usage:

```
python generate-report.py <options>
```

### Options

#### --user 

Generate report for a single user. Example:
```
python generate-report.py --user=facebook_user_id
```

#### --users

Generate report for multiple users. Pass users id separated by commas or 'all' to include all users in the report (Warning: possibly huge file)

```
python generate-report.py --users=facebook_user_id,facebook_user_id,facebook_user_id
```

## Preview 

![Example chart](https://i.imgur.com/QzieenK.png)