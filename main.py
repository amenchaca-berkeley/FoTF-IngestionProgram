import userDefined as ud
import sync
import ingestion

# Sync Files from Box with local server desktop
try:
    sync.main()
except Exception as e:
    print(e)
    print("Failed to run sync.main()!")

# Run ingestion script
try:
    ingestion.main()
except Exception as e:
    print(e)
    print("Failed to run ingestion.main()!")
