from src.core.config import Settings

settings = Settings() # type: ignore


import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = settings.BREVO_API_KEY

# Create an instance of the API class
api_instance = sib_api_v3_sdk.EmailCampaignsApi(sib_api_v3_sdk.ApiClient(configuration))


def send_email(to_email, name, sub, html_content):
    # Define the campaign settings
    email_campaigns = sib_api_v3_sdk.CreateEmailCampaign(
        name=name,
        subject=sub,
        sender={"name": settings.MAIL_FROM_NAME, "email": settings.MAIL_FROM},
        html_content=html_content,
        recipients={"listIds": [2, 7]}
    )
    # Send the campaign
    try:
        api_response = api_instance.create_email_campaign(email_campaigns)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling EmailCampaignsApi->create_email_campaign: %s\n" % e)


