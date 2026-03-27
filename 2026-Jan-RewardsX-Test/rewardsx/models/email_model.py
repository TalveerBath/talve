

# ( validation the ai and extra messages, formats the email )

# validating AI's json output 
    # "from pydantic import BaseModel which will catch if ai returns something 
    # invalid"
#enforcing required fields

# preventing extra text or whatevr 

# 
# ensuring consistent structure across the pipeline 




# email_extractor/models/reward_extraction_model.py

from pydantic import BaseModel, Field
from typing import Optional


class RewardExtractionModel(BaseModel):
    """
    Validates the AI's extracted reward information.
    Ensures consistent structure and prevents extra fields or hallucinated text.
    """

    program: str = Field(..., description="The loyalty or rewards program name.")
    points_earned: int = Field(..., description="Number of points earned from this transaction.")
    points_balance: Optional[int] = Field(None, description="Total points balance after the transaction.")
    eligible_for_redemption: Optional[bool] = Field(None, description="Whether the user can redeem points.")
    
    transaction_id: Optional[str] = Field(None, description="The transaction or receipt ID.")
    store_id: Optional[str] = Field(None, description="The store or location ID.")
    location: Optional[str] = Field(None, description="The store location name.")
    purchase_datetime: Optional[str] = Field(None, description="Purchase date and time in ISO or email format.")
    order_total: Optional[str] = Field(None, description="Total purchase amount, usually a string like '$18.52'.")

    expiry_date: Optional[str] = Field(None, description="Date when earned points expire.")
    loyalty_id: Optional[str] = Field(None, description="Customer loyalty or membership ID.")
    email: Optional[str] = Field(None, description="Customer email address found in the message.")

    class Config:
        extra = "forbid"            #  AI cannot return extra fields
        validate_assignment = True  # Validate fields even when updated


# goes in main.py to validate the AI's output after extraction and before storage or use in the app
#raw_email = parse_eml("data/emails/01_mcdonald's_rewards.eml")
#validated = EmailModel(**raw_email)
#print(validated)