get all users
GET /api/users/

Response
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

create a user
POST /api/users/
Request
{
    "name": <USER INPUT FOR NAME>,
    "username": <USER INPUT FOR USERNAME>
}

Response
{   
    "success": true,
    "data": {
        "id": <ID>,
        "name": <USER INPUT FOR NAME>,
        "username": <USER INPUT FOR USERNAME>
    }
}

get a specific user by id
GET /api/users/{user_id}/
Response
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

delete a user
DELETE /api/users/{user_id}/
Response
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

friend a user
POST /api/users/{user1_id}/friend/{user2_id}/
Response
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

get all songs in the database
GET /api/songs/
Response
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

add a song to the database
POST /api/songs/
Request
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

search for songs
POST /api/songs/search/
Request
{
    "search": <USER INPUT FOR SEARCH>
}

Response
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

get a specific song by id
POST /api/songs/{song_id}/
Response
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

add a favorite song to a user
POST /api/users/{user_id}/songs/{int:song_id}/
Response
{
    "success": true,
    "data": {
        "id": <ID>,
        "title": <USER INPUT FOR TITLE>,
        "artist": <USER INPUT FOR ARTIST>,
        "album": <USER INPUT FOR ALBUM>
    }
}

get song requests of a specific user
GET /api/users/{user_id}/requests/
Response
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

get a specific song request by id
GET /api/users/requests/{request_id}/
Response
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

create a song request for a user
POST /api/users/{user_id}/requests/
Request
{
    "genre": <USER INPUT FOR GENRE>,
    "message": <USER INPUT FOR MESSAGE>,
}

Response
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

end a song request for a user
POST /api/users/requests/{request_id}/
Response
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

create a song recommendation for a song request
POST /api/users/requests/{request_id/}recommend/{song_id}/
Request
{
    "message": <USER INPUT FOR MESSAGE>
}

Response:
{
    "success": true,
    "data": {
        "id": <ID>,
        "message": <USER INPUT FOR MESSAGE>,
        "song": [ <SERIALIZED SONG> ]
    }
}
get a specific song recommendation by id
GET /api/recommendations/{rec_id}/
Response
{
    "success": true,
    "data": {
        "id": <ID>,
        "message": <USER INPUT FOR MESSAGE>,
        "song": [ <SERIALIZED SONGS> ]      
    }
}