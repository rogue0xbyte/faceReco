import boto3

def create_collection(collection_id, region):
    # Initialize boto3 client for Rekognition
    rekognition = boto3.client('rekognition', region_name='us-east-1',
                           aws_access_key_id='KEY',
                           aws_secret_access_key='KEY')

    try:
        # Create the collection
        response = rekognition.create_collection(
            CollectionId=collection_id
        )
        print(f"Collection '{collection_id}' created successfully.")
        print(response)
    except Exception as e:
        print(f"Error creating collection: {e}")

def print_filenames_in_collection(collection_id, region):
    # Initialize boto3 client for Rekognition
    rekognition = boto3.client('rekognition', region_name='us-east-1',
                           aws_access_key_id='KEY',
                           aws_secret_access_key='KEY')

    try:
        # List faces in the collection
        response = rekognition.list_faces(CollectionId=collection_id)
        c = 0
        for face_record in response['Faces']:
            c+=1
            print(face_record)
        print(c)
    except Exception as e:
        print(f"Error listing faces: {e}")

def delete_all_faces_in_collection(collection_id, region):
    # Initialize boto3 client for Rekognition
    rekognition = boto3.client('rekognition', region_name='us-east-1',
                           aws_access_key_id='KEY',
                           aws_secret_access_key='KEY')

    try:
        # List faces in the collection
        response = rekognition.list_faces(CollectionId=collection_id)
        
        # Delete each face in the collection
        for face_record in response['Faces']:
            face_id = face_record['FaceId']
            rekognition.delete_faces(CollectionId=collection_id, FaceIds=[face_id])
        print("All faces deleted successfully.")
    except Exception as e:
        print(f"Error deleting faces: {e}")

def delete_faces_with_substring(collection_id, region, substring):
    # Initialize boto3 client for Rekognition
    rekognition = boto3.client('rekognition', region_name='us-east-1',
                           aws_access_key_id='KEY',
                           aws_secret_access_key='KEY')

    try:
        # List faces in the collection
        response = rekognition.list_faces(CollectionId=collection_id)

        # Delete faces containing the substring in their external image ID
        for face_record in response['Faces']:
            external_image_id = face_record['ExternalImageId']
            if substring in external_image_id:
                face_id = face_record['FaceId']
                rekognition.delete_faces(CollectionId=collection_id, FaceIds=[face_id])
        print(f"All faces containing '{substring}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting faces: {e}")


if __name__ == "__main__":
    # Specify the collection ID and region
    collection_id = 'face_db'
    region = 'us-east-1'

    # Create the collection
    # create_collection(collection_id, region)
    # delete_all_faces_in_collection(collection_id, region)
    print_filenames_in_collection(collection_id, region)