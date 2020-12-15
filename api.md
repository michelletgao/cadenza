# API Specification

***
## **Get all users**
**GET** /api/users/

##### Response
 ```yaml
{
    "success": true,
    "data": [
        {
            "id": <ID>,
            "name": <USER INPUT FOR NAME>,
            "username": <USER INPUT FOR USERNAME>,
            "requests": [ <SERIALIZED REQUESTS>, ... ],
            "fav_songs": [ <SERIALIZED SONGS>, ... ],
            "friends": [ <SERIALIZED USERS WITH JUST NAMES, USERNAMES>, ... ]
        },
        {
            "id": <ID>,
            "name": <USER INPUT FOR NAME>,
            "username": <USER INPUT FOR USERNAME>,
            "requests": [ <SERIALIZED REQUESTS>, ... ],
            "fav_songs": [ <SERIALIZED SONGS>, ... ],
            "friends": [ <SERIALIZED USERS WITH JUST NAMES, USERNAMES>, ... ]
        },
        ...
    ]
}
```

## **Create a user**
**POST** /api/users/

##### Request
 ```yaml
{
    "name": <USER INPUT FOR NAME>,
    "username": <USER INPUT FOR USERNAME>
}
```

##### Response

 ```yaml
{   
    "success": true,
    "data": {
        "id": <ID>,
        "name": <USER INPUT FOR NAME>,
        "username": <USER INPUT FOR USERNAME>
    }
}
```

## **Get a specific user by id**
**GET** /api/users/{user_id}/

##### Response

```yaml
{
    "success": true,
    "data": {
        "id": <ID>,
        "name": <USER INPUT FOR NAME>,
        "username": <USER INPUT FOR USERNAME>,
        "requests": [ <SERIALIZED REQUESTS>, ... ],
        "fav_songs": [ <SERIALIZED SONGS>, ... ],
        "friends": [ <SERIALIZED USERS WITH JUST NAMES, USERNAMES> ... ]
    }
}
```

## **Delete a user**
**DELETE** /api/users/{user_id}/

##### Response

```yaml
{
    "success": true,
    "data": {
        "id": <ID>,
        "name": <USER INPUT FOR NAME>,
        "username": <USER INPUT FOR USERNAME>,
        "requests": [ <SERIALIZED REQUESTS>, ... ],
        "fav_songs": [ <SERIALIZED SONGS>, ... ],
        "friends": [ <SERIALIZED USERS WITH JUST NAMES, USERNAMES> ... ]
    }
}
```

## **Friend a user**
**POST** /api/users/{user1_id}/friend/{user2_id}/

##### Response
```yaml
{
    "success": true,
    "data": {
        "id": <ID>,
        "name": <USER INPUT FOR NAME>,
        "username": <USER INPUT FOR USERNAME>,
        "friends": [
            {
                "id": <ID>,
                "name": <USER INPUT FOR NAME>,
                "username": <USER INPUT FOR USERNAME>,
            }
        ]
        
    }
}
```

## **Get all songs in the database**
**GET** /api/songs/

##### Response
```yaml
{
    "success": true,
    "data": [
        {
            "id": <ID>,
            "title": <USER INPUT FOR TITLE>,
            "artist": <USER INPUT FOR ARTIST>,
            "album": <USER INPUT FOR ALBUM>
        }
        {
            "id": <ID>,
            "title": <USER INPUT FOR TITLE>,
            "artist": <USER INPUT FOR ARTIST>,
            "album": <USER INPUT FOR ALBUM>
        }
        ...
    ]
}
```

## **Add a song to the database**
**POST** /api/songs/

##### Request
```yaml
{
    "title": <USER INPUT FOR TITLE>,
    "artist": <USER INPUT FOR ARTIST>
}

Response
{
    "success": true,
    "data": {
        "id": <ID>,
        "title": <USER INPUT FOR TITLE>,
        "artist": <USER INPUT FOR ARTIST>,
        "album": <RETRIEVED INPUT FOR ALBUM>
    }
}
```

## **Search for songs**
**POST** /api/songs/search/

##### Request
```yaml
{
    "search": <USER INPUT FOR SEARCH>
}
```

##### Response
```yaml
{   "success": true,
    "data": [
        {
            "title": <RETRIEVED INPUT FOR TITLE>,
            "artist": <RETRIEVED INPUT FOR ARTIST>,
            "album": <RETRIEVED INPUT FOR ALBUM>
        },
        {
            "title": <RETRIEVED INPUT FOR TITLE>,
            "artist": <RETRIEVED INPUT FOR ARTIST>,
            "album": <RETRIEVED INPUT FOR ALBUM>
        },
        {
            "title": <RETRIEVED INPUT FOR TITLE>,
            "artist": <RETRIEVED INPUT FOR ARTIST>,
            "album": <RETRIEVED INPUT FOR ALBUM>
        },
        ...
    ]  
}
```

## **Get a specific song by id**
**POST** /api/songs/{song_id}/

##### Response
```yaml
{
    "success": true,
    "data": [
        {
            "id": <ID>,
            "title": <USER INPUT FOR TITLE>,
            "artist": <USER INPUT FOR ARTIST>,
            "album": <USER INPUT FOR ALBUM>
        }
    ]
}
```

## **Add a favorite song to a user**
**POST** /api/users/{user_id}/songs/{int:song_id}/

##### Response
```yaml
{
    "success": true,
    "data": {
        "id": <ID>,
        "title": <USER INPUT FOR TITLE>,
        "artist": <USER INPUT FOR ARTIST>,
        "album": <USER INPUT FOR ALBUM>
    }
}
```

## **Get song requests of a specific user**
**GET** /api/users/{user_id}/requests/

##### Response
```yaml
{
    "success": true,
    "data": 
        {
            "id": <ID>,
            "genre": <USER INPUT FOR GENRE>,
            "message": <USER INPUT FOR MESSAGE>,
            "timestamp": <TIME OF REQUEST>,
            "completed": true or false,
            "recommendations": [ <SERIALIZED RECOMMENDATIONS>, ...]  
        }
}
```

## **Get a specific song request by id**
**GET** /api/users/requests/{request_id}/

##### Response
```yaml
{
    "success": true,
    "data": {
        "id": <ID>,
        "genre": <USER INPUT FOR GENRE>,
        "message": <USER INPUT FOR MESSAGE>,
        "timestamp": <TIME OF REQUEST>,
        "completed": true or false,
        "recommendations": [ <SERIALIZED RECOMMENDATIONS>, ...]
    }
}
```

## **Create a song request for a user**
**POST** /api/users/{user_id}/requests/

##### Request
```yaml
{
    "genre": <USER INPUT FOR GENRE>,
    "message": <USER INPUT FOR MESSAGE>,
}
```

##### Response
```yaml
{
    "success": true,
    "data": {
        "id": <ID>,
        "genre": <USER INPUT FOR GENRE>,
        "message": <USER INPUT FOR MESSAGE>,
        "timestamp": <TIME OF REQUEST>,
        "completed": false,
        "recommendations": []
    }
}
```

## **Create a song request for a user**
**POST** /api/users/requests/{request_id}/

##### Response
```yaml
{
    "success": true,
    "data": {
        "id": <ID>,
        "genre": <USER INPUT FOR GENRE>,
        "message": <USER INPUT FOR MESSAGE>,
        "timestamp": <TIME OF REQUEST>,
        "completed": true,
        "recommendations": [ <SERIALIZED RECOMMENDATIONS>, ...]
    }
}
```

## **Create a song recommendation for a song request**
**POST** /api/users/requests/{request_id/}recommend/{song_id}/

##### Request
```yaml
{
    "message": <USER INPUT FOR MESSAGE>
}
```

##### Response:
```yaml
{
    "success": true,
    "data": {
        "id": <ID>,
        "message": <USER INPUT FOR MESSAGE>,
        "song": [ <SERIALIZED SONG> ]
    }
}
```

## **Get a specific song recommendation by id**
**GET** /api/recommendations/{rec_id}/

##### Response
```yaml
{
    "success": true,
    "data": {
        "id": <ID>,
        "message": <USER INPUT FOR MESSAGE>,
        "song": [ <SERIALIZED SONGS> ]      
    }
}
```
