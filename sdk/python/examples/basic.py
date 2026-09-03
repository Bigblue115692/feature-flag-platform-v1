from featureflags import ClientConfig, EvaluationContext, FeatureFlagClient

client = FeatureFlagClient(
    ClientConfig(
        base_url="http://localhost",
        project_key="checkout",
        environment_key="production",
    )
)

context = EvaluationContext(
    user_id="user-107",
    attributes={
        "premium": True,
        "country": "US",
        "plan": "pro",
    },
)

if client.is_enabled("new_checkout", context):
    print("Render new checkout")
else:
    print("Render legacy checkout")
