# Lets create Guardrails to Design Safe and Trustworthy AI for -
# Use Case: When a customer seeks an AI Agent for a refund, 
# and lets set a rule on the maximum amount that someone can refund in a single transaction (like $100), 
# otherwise its an unsafe request. 

# Import Guard and Validator
from pydantic import BaseModel, Field
from guardrails.hub import ValidRange
from guardrails import Guard

# Initialize Validator
val = ValidRange(min=0, max=100, on_fail="exception")


# Create Pydantic BaseModel
class CustInfo(BaseModel):
    cust_name: str
    withdraw_amount: int = Field(validators=[val])


# Create a Guard to check for valid Pydantic output
guard = Guard.from_pydantic(output_class=CustInfo)

try:
    # Run LLM output generating JSON through guard 
    customer_name="OpenAI"
    refund_amount=150
    print (f"\nLets try to refund ${refund_amount} for customer {customer_name}.")
    cust_refund=f"""
            {{
                "cust_name": "{customer_name}",
                "withdraw_amount": {refund_amount}
            }}
    """
    guard.parse(cust_refund)
    print ("SUCCESS: Valid refund request.")
except Exception as e:
    print("FAILED: ",e)

try:
    # Run LLM output generating JSON through guard 
    customer_name="IBM"
    refund_amount=50
    print (f"\nLets try to refund ${refund_amount} for customer {customer_name}.")
    cust_refund=f"""
            {{
                "cust_name": "{customer_name}",
                "withdraw_amount": {refund_amount}
            }}
    """
    guard.parse(cust_refund)
    print ("SUCCESS: Valid refund request.")
except Exception as e:
    print("FAILED: ",e)


guard.parse(
        """
        {
            "cust_name": "customer_name",
            "withdraw_amount": 50
        }
        """
    )
