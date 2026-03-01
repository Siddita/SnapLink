from hashids import Hashids
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize with environment variables
hashids = Hashids(
    salt=os.getenv("HASH_ID_SALT"),
    min_length=int(os.getenv("MIN_LENGTH", 7))
)

def encode_id(id_int: int) -> str:
    return hashids.encode(id_int)

def decode_id(short_code: str) -> int:
    result = hashids.decode(short_code)
    # If the code is invalid, decode returns an empty tuple
    return result[0] if result else None
