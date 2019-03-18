FORMAT: 1A

# OWN RESTful API

# Group Own Request Signing

Own Request Signing works by creating a hash over the relevant parts of every request.
This hash is created with the same algorithm on the server and compared
to the hash in the request. Only if both hashes match, the request is allowed for
processing. This method not only ensures that the request is coming from who it claims
to be coming (as it includes the user specific access token), but also it ensures that
the request has not been tampered with or constructed artificially alltogether.

Specific details of requests signing are excluded from this public repository,
as for the sake of development simplification request signatures are not used in the provided examples.

# Group Discovery

This resource offers the starting point for the API. Clients should only know this URL. The response 
should provide all necessary references in the "_links" section.

## GET /

**DEPRECATED**: Request and responce data will be replaced with those of `/links`.
Use `/boards` to get users boards.

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.discoveryResponse+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 (application/vnd.uberblik.discoveryResponse+json)

    + Body
    
            {
                "boards" : [
                    { "rel": "testboard", "href": "/boards/211" },
                    { "rel": "dev-board", "href": "/boards/2263" }
                ],
                "_links": [
                    { "rel" : "self", "href": "/" },
                    { "rel" : "activities", "href" : "/activities" },
                    { "rel" : "organizations", "href" : "/organizations" },
                    { "rel" : "liveUpdates", "href" : "/opensocket"  },
                    { "rel" : "invitations", "href" : "/invitations"  }
                ]
            }
            
## GET /links

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.discoveryResponse+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 (application/vnd.uberblik.discoveryResponse+json)

    + Body
    
            {
              "_links": [
                {
                  "rel": "self",
                  "href": "/"
                },
                {
                  "rel": "boards",
                  "href": "/boards"
                },
                {
                  "rel": "activities",
                  "href": "/activities"
                },
                {
                  "rel": "organizations",
                  "href": "/organizations"
                },
                {
                  "rel": "liveUpdates",
                  "href": "/opensocket"
                },
                {
                  "rel": "invitations",
                  "href": "/invitations"
                }
              ]
            }

# Group Ping

This resource is used to check systems availability. It does not require an acces token in a request header.

`/ping/time` request returns the current time in milliseconds 
(the difference, measured in milliseconds, between the current time and midnight, January 1, 1970 UTC).

## GET /ping

+ Response 200
            
## GET /ping/time

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.time+json;charset:UTF-8

+ Response 200 (application/vnd.uberblik.time+json)

    + Body
    
            {
                "time": 1514363483621
            }  

# Group Boards

Common http codes returned by operations on boards:

+ `201` when token creation was successful
+ `200` when sucessfully retrieved or deleted a board
+ `403` returned if the token is expired, invalid or not found
+ `409` returned if the name is empty or if the invitation model is not in [ADMIN_ONLY | MEMBERS_ALLOWED] 


To assign a board to an organization during it's creation, pass organization Id as a parameter for the POST request,
e.g. to assign a new board to an organization with id=1, call `/boards{?organizationId=1` instead of `/boards`


## POST /boards

+ Request

    + Headers
    
            Accept : application/vnd.uberblik.board+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
        
    + Body
    
            {
                "board":{
                    "name": "testboard",
                    "invitationModel": "MEMBERS_ALLOWED"
                }
            }

+ Response 403

+ Response 201 (application/vnd.uberblik.board+json)

            {
                "board": {
                    "name": "testboard1",
                    "sizeX": 7,
                    "sizeY": 9,
                    "lastModified": 1512995620439,
                    "invitationModel": "MEMBERS_ALLOWED",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/242"
                        },
                        {
                            "rel": "elements",
                            "href": "/boards/242/elements"
                        },
                        {
                            "rel": "archivedElements",
                            "href": "/archive/boards/242/elements"
                        },
                        {
                            "rel": "archivedFiles",
                            "href": "/archive/boards/242/files"
                        },
                        {
                            "rel": "users",
                            "href": "/boards/242/users"
                        },
                        {
                            "rel": "owner",
                            "href": "/users/1"
                        },
                        {
                            "rel": "activities",
                            "href": "/boards/242/activities"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/242/thumbnail"
                        },
                        {
                            "rel": "posts",
                            "href": "/boards/242/posts"
                        },
                        {
                            "rel": "invitedUsers",
                            "href": "/boards/242/invitedUsers"
                        },
                        {
                            "rel": "quota",
                            "href": "/boards/242/quota"
                        },
                        {
                            "rel": "invitations",
                            "href": "/invitations"
                        },
                        {
                            "rel": "organizations",
                            "href": "/organizations"
                        }
                    ]
                }
            }


## POST /boards?organizationId={organizationId}

+ Request

    + Headers
    
            Accept : application/vnd.uberblik.board+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
        
    + Body
    
            {
                "board":{
                    "name": "testboard",
                    "invitationModel": "MEMBERS_ALLOWED"
                }
            }

+ Response 403

+ Response 201 (application/vnd.uberblik.board+json)

            {
                "board": {
                    "name": "testboard1",
                    "sizeX": 7,
                    "sizeY": 9,
                    "lastModified": 1512995531734,
                    "invitationModel": "MEMBERS_ALLOWED",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/241"
                        },
                        {
                            "rel": "elements",
                            "href": "/boards/241/elements"
                        },
                        {
                            "rel": "archivedElements",
                            "href": "/archive/boards/241/elements"
                        },
                        {
                            "rel": "archivedFiles",
                            "href": "/archive/boards/241/files"
                        },
                        {
                            "rel": "users",
                            "href": "/boards/241/users"
                        },
                        {
                            "rel": "owner",
                            "href": "/users/1"
                        },
                        {
                            "rel": "activities",
                            "href": "/boards/241/activities"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/241/thumbnail"
                        },
                        {
                            "rel": "posts",
                            "href": "/boards/241/posts"
                        },
                        {
                            "rel": "invitedUsers",
                            "href": "/boards/241/invitedUsers"
                        },
                        {
                            "rel": "quota",
                            "href": "/boards/241/quota"
                        },
                        {
                            "rel": "invitations",
                            "href": "/invitations"
                        },
                        {
                            "rel": "organizations",
                            "href": "/organizations"
                        },
                        {
                            "rel": "organization",
                            "href": "/organizations/1"
                        }
                    ]
                }
            }
            

## GET /boards?limit={limit}&offset={offset}&order={order}

Gets a limited number of boards (as passed in limit query parameter) of a logged in user, 
skipping several (as passed in offset query parameter) boards before beginning the return of boards.

If a `limit` count is given, no more than that many rows will be returned (but possibly less,
if the query itself yields less rows). Negative or equal 0 limit is the same as omitting the `limit` clause.

Parameter `offset` says to skip that many rows before beginning to return rows. 
`offset` <=0 is the same as omitting the `offset` clause. If both `offset` and `limit` appear 
then `offset` rows are skipped before starting to count the LIMIT rows that are returned.

`order` parameter repsesents the order in which boards will be returned.
By default (if the `order` parameter were not passed) boards are returned sorted the time of last modification made on it in descending order (`limit=lastmodified`).
If you want to get boards sorted by board ids in descending order, use `order=boardid`.
Only `boardid` and `lastmodified` are valid values for the `order` parameter. If something else is passed,
`lastmodified` value will be set.

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.boards+json;charset:UTF-8

+ Response 200 (application/vnd.uberblik.boards+json)

    + Body
    
            {
                "boards":[
                    {
                        "rel":"Demo Board Name",
                        "href":"/boards/281"
                    },
                    {
                        "rel":"testboard1",
                        "href":"/boards/261"
                    },
                    {
                        "rel":"Welcome to OWN",
                        "href":"/boards/1"
                    }
                ]
            }

## GET /boards?limit={limit}&offset={offset}&order={order}&includeDetails=true

Gets a limited number of boards (as passed in limit query parameter) of a logged in user, 
skipping several (as passed in offset query parameter) boards before beginning the return of boards.

If a `limit` count is given, no more than that many rows will be returned (but possibly less,
if the query itself yields less rows). Negative or equal 0 limit is the same as omitting the `limit` clause.

Parameter `offset` says to skip that many rows before beginning to return rows. 
`offset` <=0 is the same as omitting the `offset` clause. If both `offset` and `limit` appear 
then `offset` rows are skipped before starting to count the LIMIT rows that are returned.

`order` parameter repsesents the order in which boards will be returned.
By default (if the `order` parameter were not passed) boards are returned sorted the time of last modification made on it in descending order (`limit=lastmodified`).
If you want to get boards sorted by board ids in descending order, use `order=boardid`.
Only `boardid` and `lastmodified` are valid values for the `order` parameter. If something else is passed,
`lastmodified` value will be set.

`includeDetails` parameter is not obligatory.
If it is set to `true`, then request not only returns boards names and ids, but also detailed data 
about boards themselves, and their sub-entities, i.e. info about elements (incl. filesCount, unviewedFilesCount, 
and agentTaskId), and files with viewing info for the user who sent a request.

**NOTE:** Measure the performance of the request, before usage of `includeDetails` parameter.
As of 06.02.2019 query to the production database to get info about 20 boards takes approximately 1.75 seconds.

Returned results is sorted in the following order:
* boards by `id` or `last_modified`, depending on the `order` parameter, in the descending order
* elements by `id` in the descending order
* files by `index` in the descending order
* files by `id` in the descending order 
(in case several files have the same index, which might, unfortunately, be the case)

`embeddedLink` parameter contains a link for those elements in which file with highest index is a link, 
url of which starts with `https://embed.own.space`.

`unviewedFileCount` parameter states how many files in the element user has not seen yet.

`viewed` parameter states whether user viewed file already or not.

`organizationId` parameter contains id of the organization the board belongs to, 
or `none` if the board does not belong to an organization.


+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.boards+json;charset:UTF-8

+ Response 200 (application/vnd.uberblik.boards+json)

    + Body
    
            {
              "boards": [
                {
                  "id": 2,
                  "name": "Welcome to OWN",
                  "sizeX": 7,
                  "sizeY": 9,
                  "lastModified": 1549411638247,
                  "invitationModel": "MEMBERS_ALLOWED",
                  "organizationId": null,
                  "elements": [
                    {
                      "id": 202,
                      "archived": false,
                      "sizeX": 1,
                      "sizeY": 1,
                      "posX": 3,
                      "posY": 1,
                      "caption": "",
                      "type": "MultiInput",
                      "fileCount": 3,
                      "unviewedFileCount": 0,
                      "agentTaskId": null,
                      "embeddedLink": null,
                      "files": [
                        {
                          "id": 387,
                          "name": "DSC_2186.jpg",
                          "fileType": "image/jpeg",
                          "index": 2,
                          "viewed": true
                        },
                        {
                          "id": 386,
                          "name": "2013-08-05 21-50-06_1375776132.JPG",
                          "fileType": "image/jpeg",
                          "index": 1,
                          "viewed": true
                        },
                        {
                          "id": 385,
                          "name": "photo_2016-10-20_01-31-42.jpg",
                          "fileType": "image/jpeg",
                          "index": 0,
                          "viewed": true
                        }
                      ]
                    },
                    {
                      "id": 201,
                      "archived": false,
                      "sizeX": 1,
                      "sizeY": 1,
                      "posX": 2,
                      "posY": 1,
                      "caption": "",
                      "type": "MultiInput",
                      "fileCount": 1,
                      "unviewedFileCount": 0,
                      "agentTaskId": null,
                      "embeddedLink": null,
                      "files": [
                        {
                          "id": 384,
                          "name": "photo_2016-10-20_01-31-42.jpg",
                          "fileType": "image/jpeg",
                          "index": 0,
                          "viewed": true
                        }
                      ]
                    },
                    {
                      "id": 181,
                      "archived": false,
                      "sizeX": 6,
                      "sizeY": 5,
                      "posX": 1,
                      "posY": 2,
                      "caption": "",
                      "type": "MultiInput",
                      "fileCount": 2,
                      "unviewedFileCount": 0,
                      "agentTaskId": null,
                      "embeddedLink": "https://embed.own.space/data/",
                      "files": [
                        {
                          "id": 401,
                          "name": "Graph2d | Performance",
                          "fileType": "application/vnd.uberblik.htmlReference",
                          "index": 4,
                          "viewed": true
                        },
                        {
                          "id": 383,
                          "name": "2013-08-05 21-50-06_1375776132.JPG",
                          "fileType": "image/jpeg",
                          "index": 1,
                          "viewed": true
                        }
                      ]
                    }
                  ]
                },
                {
                  "id": 41,
                  "name": "11",
                  "sizeX": 7,
                  "sizeY": 9,
                  "lastModified": 1549385009713,
                  "invitationModel": "MEMBERS_ALLOWED",
                  "organizationId": 2,
                  "elements": []
                },
                {
                  "id": 1,
                  "name": "Welcome to OWN",
                  "sizeX": 7,
                  "sizeY": 9,
                  "lastModified": 1549384947764,
                  "invitationModel": "MEMBERS_ALLOWED",
                  "organizationId": null,
                  "elements": [
                    {
                      "id": 121,
                      "archived": false,
                      "sizeX": 1,
                      "sizeY": 1,
                      "posX": 3,
                      "posY": 2,
                      "caption": "",
                      "type": "MultiInput",
                      "fileCount": 0,
                      "unviewedFileCount": 0,
                      "agentTaskId": null,
                      "embeddedLink": null,
                      "files": []
                    },
                    {
                      "id": 102,
                      "archived": false,
                      "sizeX": 1,
                      "sizeY": 1,
                      "posX": 7,
                      "posY": 1,
                      "caption": "",
                      "type": "MultiInput",
                      "fileCount": 1,
                      "unviewedFileCount": 0,
                      "agentTaskId": null,
                      "embeddedLink": null,
                      "files": [
                        {
                          "id": 325,
                          "name": "photo_2016-10-20_01-31-42.jpg",
                          "fileType": "image/jpeg",
                          "index": 0,
                          "viewed": true
                        }
                      ]
                    },
                    {
                      "id": 101,
                      "archived": false,
                      "sizeX": 1,
                      "sizeY": 1,
                      "posX": 6,
                      "posY": 1,
                      "caption": "",
                      "type": "MultiInput",
                      "fileCount": 1,
                      "unviewedFileCount": 0,
                      "agentTaskId": null,
                      "embeddedLink": null,
                      "files": [
                        {
                          "id": 324,
                          "name": "photo_2016-10-20_01-31-42.jpg",
                          "fileType": "image/jpeg",
                          "index": 0,
                          "viewed": true
                        }
                      ]
                    },
                    {
                      "id": 81,
                      "archived": false,
                      "sizeX": 1,
                      "sizeY": 1,
                      "posX": 2,
                      "posY": 2,
                      "caption": "",
                      "type": "MultiInput",
                      "fileCount": 3,
                      "unviewedFileCount": 0,
                      "agentTaskId": null,
                      "embeddedLink": null,
                      "files": [
                        {
                          "id": 43,
                          "name": "Three New Breakthroughs to Advance Metal Addive Manufacturing | IndustryWeek",
                          "fileType": "application/vnd.uberblik.htmlReference",
                          "index": 2,
                          "viewed": true
                        },
                        {
                          "id": 42,
                          "name": "The BIG IDEAS for UV + EB Technology Conference is the Place to Learn About Photopolymers and 3D Printing | 3DPrint.com | The Voice of 3D Printing / Additive Manufacturing",
                          "fileType": "application/vnd.uberblik.htmlReference",
                          "index": 1,
                          "viewed": true
                        },
                        {
                          "id": 41,
                          "name": "Page not found - 3D Printing Industry",
                          "fileType": "application/vnd.uberblik.htmlReference",
                          "index": 0,
                          "viewed": true
                        }
                      ]
                    },
                    {
                      "id": 1,
                      "archived": false,
                      "sizeX": 7,
                      "sizeY": 7,
                      "posX": 1,
                      "posY": 3,
                      "caption": "",
                      "type": "MultiInput",
                      "fileCount": 5,
                      "unviewedFileCount": 1,
                      "agentTaskId": null,
                      "embeddedLink": null,
                      "files": [
                        {
                          "id": 301,
                          "name": "Название на Русском.",
                          "fileType": "application/vnd.uberblik.htmlReference",
                          "index": 59,
                          "viewed": true
                        },
                        {
                          "id": 281,
                          "name": "photo_2016-10-20_01-31-42.jpg",
                          "fileType": "image/jpeg",
                          "index": 58,
                          "viewed": true
                        },
                        {
                          "id": 3,
                          "name": "BarChart",
                          "fileType": "application/vnd.uberblik.chart+json",
                          "index": 2,
                          "viewed": true
                        },
                        {
                          "id": 2,
                          "name": "http://mi.com",
                          "fileType": "application/vnd.uberblik.htmlReference",
                          "index": 1,
                          "viewed": true
                        },
                        {
                          "id": 1,
                          "name": "Screenshot from 2019-01-15 12-19-05.png",
                          "fileType": "image/png",
                          "index": 0,
                          "viewed": true
                        }
                      ]
                    }
                  ]
                },
                {
                  "id": 21,
                  "name": "wadawdwada",
                  "sizeX": 7,
                  "sizeY": 9,
                  "lastModified": 1548867538308,
                  "invitationModel": "MEMBERS_ALLOWED",
                  "organizationId": 3,
                  "elements": [
                    {
                      "id": 141,
                      "archived": false,
                      "sizeX": 1,
                      "sizeY": 1,
                      "posX": 1,
                      "posY": 1,
                      "caption": "",
                      "type": "MultiInput",
                      "fileCount": 0,
                      "unviewedFileCount": 0,
                      "agentTaskId": 21,
                      "embeddedLink": null,
                      "files": []
                    }
                  ]
                }
              ]
            }

## GET /boards/count

Gets a quantity of boards for the currently logged in user

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.boardsCount+json;charset:UTF-8

+ Response 200 (application/vnd.uberblik.boardsCount+json)

    + Body

            {
                "boardsCount":3
            }


## GET /boards/{boardId}

A link with rel==`organization` is returned only if this board is assigned to some organization.

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.board+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
                        
+ Response 200 (application/vnd.uberblik.board+json)

    + Body
    
            {
                "board":{
                    "id":462,
                    "name":"testboard Hogwarts 2",
                    "sizeX":7,
                    "sizeY":9,
                    "lastModified":1522311125887,
                    "invitationModel":"MEMBERS_ALLOWED",
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/462"
                        },
                        {
                            "rel":"elements",
                            "href":"/boards/462/elements"
                        },
                        {
                            "rel":"archivedElements",
                            "href":"/archive/boards/462/elements"
                        },
                        {
                            "rel":"archivedFiles",
                            "href":"/archive/boards/462/files"
                        },
                        {
                            "rel":"users",
                            "href":"/boards/462/users"
                        },
                        {
                            "rel":"owner",
                            "href":"/users/1"
                        },
                        {
                            "rel":"activities",
                            "href":"/boards/462/activities"
                        },
                        {
                            "rel":"thumbnail",
                            "href":"/boards/462/thumbnail"
                        },
                        {
                            "rel":"posts",
                            "href":"/boards/462/posts"
                        },
                        {
                            "rel":"invitedUsers",
                            "href":"/boards/462/invitedUsers"
                        },
                        {
                            "rel":"quota",
                            "href":"/boards/462/quota"
                        },
                        {
                            "rel":"invitations",
                            "href":"/invitations"
                        },
                        {
                            "rel":"organizations",
                            "href":"/organizations"
                        },
                        {
                            "rel":"organization",
                            "href":"/organizations/2"
                        }
                    ]
                }
            }
            
## PUT /boards/{boardId}

+ Request
    + Headers
    
            Accept : application/vnd.uberblik.board+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

    + Body
    
            {
                "board": {
                    "name" : "testboard",
                    "invitationModel": "ADMIN_ONLY"
                    }
            }

                        
+ Response 200 (application/vnd.uberblik.board+json)

    + Body
    
            {
                "board": {
                    "name" : "testboard",
                    "sizeX" : "8",
                    "sizeY" : "10",
                    "invitationModel": "ADMIN_ONLY",
                    "lastModified": 1397023355854,
                    "_links":
                        [
                            { "rel": "elements", "href": "/boards/211/elements" },
                            { "rel": "archivedElements", "href": "/archive/boards/211/elements" },
                            { "rel": "archivedFiles", "href": "/archive/boards/211/files" },
                            { "rel": "users", "href": "/boards/211/users" },
                            { "rel": "activities", "href": "/boards/211/activities" },
                            { "rel": "self", "href": "/boards/211" },
                            { "rel": "thumbnail",  "href": "/boards/21/thumbnail" },
                            { "rel": "posts",  "href": "/boards/21/posts" },
                            { "rel": "invitedUsers", "href": "/boards/211/invitedUsers" },
                            { "rel": "quota", "href": "/boards/211/quota" },
                            { "rel": "invitations", "href": "/invitations" },
                            { "rel" : "owner", "href" : "/users/2" }
                        ]
                }
            }


## DELETE /boards/{boardId}

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.board+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 ()


# Group Board thumbnails 

Board thumbnails (and all other image resources) are not protected. Often, the path to these
images is injected into the HTML code, therefore no custom headers can be applied to the 
request.<br>
Common http codes returned by operations on board thumbnails:

+ `200` when sucessfully retrieved a thumbnail


## GET /boards/{boardId}/thumbnail

+ Request
    + Headers
    
                Accept: image/jpeg


+ Response 200 (image/jpeg)
    
                2345f13463gg4nbbfgfbg3...



# Group Board users 

Common http codes returned by operations on board users:

+ `200` when sucessfully retrieved board users
+ `201` when successfully added a new user to this board
+ `403` returned if the token is expired, invalid or not found


## GET /boards/{boardId}/users

`inviterId` is id of the user who invited given user to the board with id=`boardId`.

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.users+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 (application/vnd.uberblik.users+json)

    + Body
    
            {
              "users": [
                {
                  "id": 1,
                  "email": "nedorezov@own.space",
                  "firstName": "Aleksandr",
                  "lastName": "Nedorezov",
                  "displayName": "Aleksandr",
                  "locale": "en",
                  "dailyActivityDigest": true,
                  "status": "ACTIVE",
                  "viewIntroductoryInstructions": false,
                  "_links": [
                    {
                      "rel": "self",
                      "href": "/users/1"
                    },
                    {
                      "rel": "profileThumbnail",
                      "href": "/users/1/profileThumbnail"
                    },
                    {
                      "rel": "boardUser",
                      "href": "/boards/1/users/1"
                    }
                  ],
                  "isOwner": true,
                  "inviterId": 1
                },
                {
                  "id": 2,
                  "email": "test@test.own.space",
                  "firstName": "test",
                  "lastName": "user",
                  "displayName": "test",
                  "locale": "en",
                  "dailyActivityDigest": true,
                  "status": "ACTIVE",
                  "viewIntroductoryInstructions": false,
                  "_links": [
                    {
                      "rel": "self",
                      "href": "/users/2"
                    },
                    {
                      "rel": "profileThumbnail",
                      "href": "/users/2/profileThumbnail"
                    },
                    {
                      "rel": "boardUser",
                      "href": "/boards/1/users/2"
                    }
                  ],
                  "isOwner": false,
                  "inviterId": 1
                },
                {
                  "id": 3,
                  "email": "test2@test.own.space",
                  "firstName": "test2",
                  "lastName": "user",
                  "displayName": "test2",
                  "locale": "en",
                  "dailyActivityDigest": true,
                  "status": "ACTIVE",
                  "viewIntroductoryInstructions": false,
                  "_links": [
                    {
                      "rel": "self",
                      "href": "/users/3"
                    },
                    {
                      "rel": "profileThumbnail",
                      "href": "/users/3/profileThumbnail"
                    },
                    {
                      "rel": "boardUser",
                      "href": "/boards/1/users/3"
                    }
                  ],
                  "isOwner": false,
                  "inviterId": 2
                }
              ],
              "_links": [
                {
                  "rel": "self",
                  "href": "/boards/1/users"
                }
              ]
            }

## GET /boards/{boardId}/users?includeAgentSubscriptionsData=true

`inviterId` is id of the user who invited given user to the board with id=`boardId`.

**NOTE:** `inviterId` can be `null`! (If user modified their primary email address)

`ownerId`==`true`, means that user is a creator of the board with id=`boardId`.

Possible subscription provider types are `USER`, and `ORGANIZATION`.

If `subscription.id` == `null` that means the agent is either a board owner, 
or was invited to the board by the user without subscription, but with elevated privileges, i.e. OWN.space team member.

If `subscription.id` == `null`, 
then `subscription.expirationDate`, `subscription.capacity`, 
and `subscription.performedQueries` will also have `null` value.

Possible member types are `USER`, and `AGENT`.

**NOTE:** Agents always go after regular users in the list.

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.users+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 (application/vnd.uberblik.users+json)

    + Body
    
            {
                "users": [
                    {
                        "id": 1,
                        "firstName": "Aleksandr",
                        "lastName": "Nedorezov",
                        "email": "nedorezov@own.space",
                        "isOwner": true,
                        "inviterId": 1,
                        "memberType": "USER"
                    },
                    {
                        "id": 12,
                        "firstName": "Sebastian",
                        "lastName": "Denef",
                        "email": "denef@own.space",
                        "isOwner": false,
                        "inviterId": 1,
                        "memberType": "USER"
                    },
                    {
                        "id": 21,
                        "firstName": "Test",
                        "lastName": "Agent",
                        "email": "test111@kittens.com",
                        "isOwner": false,
                        "inviterId": 1,
                        "memberType": "AGENT",
                        "subscription": {
                            "id": null,
                            "agentDataId": 61,
                            "subscriptionProviderType": "USER",
                            "subscriptionProviderId": 1,
                            "subscriptionProviderName": "Aleksandr Nedorezov",
                            "expirationDate": null,
                            "capacity": null,
                            "performedQueries": null
                        }
                    },
                    {
                        "id": 24,
                        "firstName": "Test",
                        "lastName": "Agent 2",
                        "email": "test222@kittens.com",
                        "isOwner": false,
                        "inviterId": 1,
                        "memberType": "AGENT",
                        "subscription": {
                            "id": 23,
                            "agentDataId": 61,
                            "subscriptionProviderType": "USER",
                            "subscriptionProviderId": 1,
                            "subscriptionProviderName": "Aleksandr Nedorezov",
                            "expirationDate": 1573897245049,
                            "capacity": 10,
                            "performedQueries": 7
                        }
                    },
                    {
                        "id": 42,
                        "firstName": "Cute Pictures Provider",
                        "lastName": "Agent",
                        "email": "cpp@kittens.com",
                        "isOwner": false,
                        "inviterId": 21,
                        "memberType": "AGENT",
                        "subscription": {
                            "id": 31,
                            "agentDataId": 61,
                            "subscriptionProviderType": "ORGANIZATION",
                            "subscriptionProviderId": 12345,
                            "subscriptionProviderName": "OWN.space",
                            "expirationDate": 1573897206049,
                            "capacity": 25,
                            "performedQueries": 12
                        }
                    }
                ]
            }

## GET /boards/{boardId}/invitedUsers

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.users+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 (application/vnd.uberblik.users+json)

    + Body
    
            {
                "users": [
                    { 
                        "displayText" : "Marcelo",
                        "firstName" : "Marcelo",
                        "lastName": "Emmerich",
                        "email": "marcelo.emmerich@gmail.com"
                        "isOwner": false,
                        "_links" : 
                        [
                            { "rel" : "profileThumbnail", "href" : "/users/1/profileThumbnail" },
                            { "rel" : "self", "href" : "/users/1" },
                            { "rel" : "boardUser", "href" : "/boards/211/users/194652" }
                        ] 
                    },
                    { 
                        "displayText" : "Leonardo",
                        "firstName" : "Leonardo",
                        "lastName": "Ramirez",
                        "email": "leonardo.ramirez@zv.fraunhofer.de"
                        "isOwner": false,
                        "_links" : 
                        [
                            { "rel" : "profileThumbnail", "href" : "/users/2/profileThumbnail" },
                            { "rel" : "self", "href" : "/users/2" },
                            { "rel" : "boardUser", "href" : "/boards/211/users/291173" }
                        ] 
                    }
                ],
                "_links":
                [
                    { "rel": "self", "href": "/boards/211/invitedUsers" },
                ]
            }
            
## DELETE /boards/{boardId}/users/{userId}

Removes a user from a board. 

Board owners can remove anyone from the board. 

A board owner can't be removed from the board.

Inviters can remove invitees from board.

Error codes:

+ `409` if a user is not a members of a board, or if someone tries to remove an owner of a board.
+ `404` if userId is an id of a user who is not a member of a board, and was not invited to the board.


+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.user+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 ()

    + Body
    
# Group Board quota

## GET /boards/{boardId}/quota

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.boardquota+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 (application/vnd.uberblik.boardquota+json)

    + Body
    
            {
                "boardQuota": 
                    { 
                        "capacity" : "100000000",
                        "freeSpace" : "70000000",
                        "_links" : 
                        [
                            { "rel" : "self", "href" : "/boards/211/quota" }
                        ] 
                    }
            }

# Group Invitations

When an invitation is created, the system will send out an email to each of the 
invitees. This email will contain a link that points to the client. The client
will then trigger the addition of the user to the board specified in the 
invitation link. The link looks like this:

``https://www.uberblik.com/invite?invitation=g6f3gnrbgd6x43jx&token=7t267b5btw64c5b4w6c5bw``

Where invitation is the base64 encoded URI to the invitation, i.e. 
'/invitations/123/' and token is a temporary token used to match the
user on the server-side.

When an invitation is sent out, the system supports the following cases:

### Invitee has valid access token
Once the client receives such an invitation request, it will issue a PATCH to the
invitation passed with status "accepted". The server will match the current user
with the invitation. If the user matches, the server will add this user to the
board stored in the invitation.

### Invitee has no valid access token
In this case the client presents a page where the user can either register or
login to the system and then retrieve an access token. If this succeeds, the flow 
continues as exoplained above.

If an invitation for the same email and board gets created again, the first 
invitation will be automatically deleted. 

Common http codes returned by operations on invitations:

+ `201` when sucessfully created a new invitation
+ `200` when successfully deleting or updating an invitation
+ `400` when the PATCH request omits the extra invitation-token header
+ `409` when invitation has already been accepted, user is already member/or owner of board 
+ `404` when invitation can't be found (or has been already deleted), board/invitator urls are invalid
+ `403` returned if the token is expired, invalid or not found

List of x-uberblik-error messages:

+ `400` 
    + "400001 Invalid board"
+ `409` 
    + "409001 Invitation rejected: a user with email $EMAIL is already member or owner of board: $BOARD_ID"
    + "409002 Invitation has already been accepted."
    + "409003 User is already member of board."
    + "409004 User is owner of board.",
    + "409005 Self invited user already has an account"
    + "409006 Self invitation was not meant for this address"
+ `404`
    + "404001 Invalid board url"
+ `403`
    + "403001 Email already exists."
    + "403002 Invitation token not sent."
    + "403003 Invalid invitation token"



## POST /invitations
+ Request
    + Headers
            
            Accept: application/vnd.uberblik.invitation+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

    + Body

            {
                "invitation": {
                    "inviteeFirstName" : "Marcelo",
                    "inviteeLastName" : "Emmerich"
                    "inviteeEmail" : "test@test.com",
                    "subject" : "uberblik invitation",
                    "message" : "Hi there, please join uberblik",
                    "board" : "/boards/235634"
                }
            }
        
        
+ Response 201

    + Body 
    
            {
                "invitation": {
                    "inviterName": "Aleksandr",
                    "inviteeEmail": "facebook@gmailmic.com",
                    "inviteeFirstName": "Ololo",
                    "inviteeLastName": "Olololo",
                    "inviteeHasAccount": true,
                    "isSelfInvitation": false,
                    "message": "Dear All,\n\nI'd like to invite you to join the OWN board: Demo Board Name\n\nBest Wishes,\nAleksandr Nedorezov",
                    "boardName": "Demo Board Name",
                    "subject": "Let's do this together!",
                    "board": "/boards/281",
                    "status": "created",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/invitations/81"
                        }
                    ]
                }
            }
            
## POST /selfInvitations
+ Request
    + Headers
            
            Accept: application/vnd.uberblik.selfInvitation+json;charset:UTF-8

    + Body

            {
                "invitation": {
                    "inviteeFirstName" : "Marcelo",
                    "inviteeLastName" : "Emmerich",
                    "inviteeEmail" : "test@test.com"
                }
            }
        
        
+ Response 201

    + Body 
    
            {
                "invitation": {
                    "inviterName": "Marcelo",
                    "inviteeEmail": "test@test.com",
                    "inviteeFirstName": "Marcelo",
                    "inviteeLastName": "Emmerich",
                    "inviteeHasAccount": false,
                    "isSelfInvitation": true,
                    "message": "",
                    "boardName": "Welcome to OWN",
                    "subject": "One last step",
                    "board": "/boards/361",
                    "status": "created",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/invitations/101"
                        }
                    ]
                }
            }

            
## PATCH /invitations/{invitationId}

+ Request 
    + Headers
    
            Content-Type : application/vnd.uberblik.invitation+json
            Accept: application/vnd.uberblik.invitation+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            invitation-token: 7t267b5btw64c5b4w6c5bw

    + Body
    
            {
                "invitation" : 
                {
                    "status" : "accepted"
                }
            }
            

+ Response 200 (application/vnd.uberblik.invitation+json)

    + Body 
    
            {
                "invitation": {
                    "inviterName": "Aleksandr",
                    "inviteeEmail": "facebook@gmailmic.com",
                    "inviteeFirstName": "Ololo",
                    "inviteeLastName": "Olololo",
                    "inviteeHasAccount": true,
                    "isSelfInvitation": false,
                    "message": "Dear All,\n\nI'd like to invite you to join the OWN board: Demo Board Name\n\nBest Wishes,\nAleksandr Nedorezov",
                    "boardName": "Demo Board Name",
                    "subject": "Let's do this together!",
                    "board": "/boards/281",
                    "status": "created",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/invitations/81"
                        }
                    ]
                }
            }

## GET /invitations/{invitationId}

+ Request 
    + Headers
    
            Content-Type : */*
            Accept: application/vnd.uberblik.invitation+json;charset:UTF-8
            invitation-token: 7t267b5btw64c5b4w6c5bw

+ Response 200 (application/vnd.uberblik.invitation+json)

    + Body 
    
            {
                "invitation": {
                    "inviterName": "Aleksandr",
                    "inviteeEmail": "facebook@gmailmic.com",
                    "inviteeFirstName": "Ololo",
                    "inviteeLastName": "Olololo",
                    "inviteeHasAccount": true,
                    "isSelfInvitation": false,
                    "message": "Dear All,\n\nI'd like to invite you to join the OWN board: Demo Board Name\n\nBest Wishes,\nAleksandr Nedorezov",
                    "boardName": "Demo Board Name",
                    "subject": "Let's do this together!",
                    "board": "/boards/281",
                    "status": "created",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/invitations/81"
                        }
                    ]
                }
            }

            
            
# Group Password Reset Requests

When a user forgets his password, a new one can be requested. Requesting a new password does 
not invalidate the current password of a user, it only generates a token that allows to 
set a new password.

Note that this resource is not protected. It can be called without an access token and 
without authentication.

Once a new password reset request is generated, the backend sends an email to the address
specified if it belongs to an existing user. The Email contains a link that the client will use
to generate a new access token. The format of the link is

``https://www.uberblik.com/resetPassword?user=%2Fusers%2F3453&token=7t267b5btw64c5b4w6c5bw``


Common http codes returned by operations on passwordResetRequests:

+ `201` when sucessfully created a new passwordResetRequests
+ `410` when the email is not known to the system


## POST /passwordResetRequests

+ Request

    + Headers 
    
            Accept: application/vnd.uberblik.passwordResetRequest+json;charset:UTF-8
            
    + Body
    
            {
                "passwordResetRequest" : {
                    "email" : "test@test.com"
                }
            }
            
            
+ Response 201

+ Response 410


# Group Users

Common http codes returned by operations on users:

+ `200` when sucessfully retrieved users
+ `201` when successfully added a new user or a new profile thumbnail
+ `400` when a user with the specified email already exists
+ `403` returned if the token is expired, invalid or not found

## POST /users

If new user registers via invitation, client has to send invitation-token along

+ Request

    + Headers
    
            invitation-token: $werwwer35345weqr
            Accept: application/vnd.uberblik.user+json;charset:UTF-8

    + Body
    
            {
                "user": {
                    "displayName" : "Marcelo",
                    "firstName" : "Marcelo",
                    "lastName": "Emmerich",
                    "email": "marcelo.emmerich@gmail.com",
                    "password": "wer345&$5efr"
                }
            }

+ Response 201

    + Body
    
            { 
                "user": { 
                        "displayName" : "Marcelo",
                        "firstName" : "Marcelo",
                        "lastName": "Emmerich",
                        "email": "marcelo.emmerich@gmail.com",
                        "locale" : "en",
                        "dailyActivityDigest": true,
                        "status": "ACTIVE",
                        "viewIntroductoryInstructions": false,
                        "_links" : 
                        [
                            { "rel" : "profileThumbnail", "href" : "/users/1/profileThumbnail" },
                            { "rel" : "self", "href" : "/users/1" }
                        ] 
                }
            }

## PUT /users/{userId}

JSON with any of the fields given in requests body (not necessary all of them), will also be a valid body for this request. Therefore, in the request body, you may only pass those user parameters, which you want to modify.

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.user+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

    + Body
    
            {
                "user": {
                    "displayName" : "Marcelo",
                    "firstName" : "Marcelo",
                    "lastName": "Emmerich",
                    "locale" : "de",
                    "dailyActivityDigest": true
                }
            }

+ Response 200

    + Body
    
            {
                "user": {
                    "email": "nedorezov@own.space",
                    "firstName": "Aleksandr",
                    "lastName": "Nedorezov",
                    "displayName": "Aleksandr",
                    "locale": "en",
                    "dailyActivityDigest": true,
                    "status": "ACTIVE",
                    "viewIntroductoryInstructions": false,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/users/1"
                        },
                        {
                            "rel": "profileThumbnail",
                            "href": "/users/1/profileThumbnail"
                        },
                        {
                            "rel": "quota",
                            "href": "/users/1/quota"
                        }
                    ]
                }
            }


## PATCH /users/{userId}

Used for replacing the password of a user. In this case, no `access-token` is required. Instead, the client has 
to add a `reset-password-token`. If there is an active `resetPasswordRequest` for this user and
the tokens match, the request passes and the password is updated, otherwise the response
is a HTTP 403. Only the field `password` can be updated, any other fields in the request will be ignored.


+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.user+json;charset:UTF-8
            reset-password-token : i28yn4v2qn3458cn3478bqv8nc

    + Body
    
            {
                "user": {
                    "password": "abc123"
                }
            }

+ Response 200

    + Body
    
            {
                "user": {
                    "email": "nedorezov@own.space",
                    "firstName": "Aleksandr",
                    "lastName": "Nedorezov",
                    "displayName": "Aleksandr",
                    "locale": "en",
                    "dailyActivityDigest": true,
                    "status": "ACTIVE",
                    "viewIntroductoryInstructions": false,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/users/1"
                        },
                        {
                            "rel": "profileThumbnail",
                            "href": "/users/1/profileThumbnail"
                        },
                        {
                            "rel": "quota",
                            "href": "/users/1/quota"
                        }
                    ]
                }
            }


## GET /users/{userId}
+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.user+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200

    + Body
    
            {
                "user": {
                    "email": "nedorezov@own.space",
                    "firstName": "Aleksandr",
                    "lastName": "Nedorezov",
                    "displayName": "Aleksandr",
                    "locale": "en",
                    "dailyActivityDigest": true,
                    "status": "ACTIVE",
                    "viewIntroductoryInstructions": false,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/users/1"
                        },
                        {
                            "rel": "profileThumbnail",
                            "href": "/users/1/profileThumbnail"
                        },
                        {
                            "rel": "quota",
                            "href": "/users/1/quota"
                        }
                    ]
                }
            }

## GET /users/{userId}/quota

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.userquota+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 (application/vnd.uberblik.userquota+json)

    + Body
    
            {
                "userQuota": [
                    { 
                        "maxNumberOfOwnedBoards" : 10,
                        "ownedBoards" : 6,
                        "_links" : 
                        [
                            { "rel" : "self", "href" : "/users/1/userQuota" }
                        ] 
                    }
                ]
            }


## GET /users/{userId}/profileThumbnail

+ Request 
    + Headers
    
            Accept: image/jpeg

+ Response 200 (image/jpeg)

    + Headers
    
            Content-Size: 346272345

    + Body
    
            gh6f6g346gf3g46r346rr4h9d273hd293hh32...

## PUT /users/{userId}/profileThumbnail

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.user+json
            access-token: uywg87gw6gf6g468gf46g4f6g34f4f4
        
    + Body
    
            gh6f6g346gf3g46r346rr4h9d273hd293hh32...

+ Response 201 (Created)


## GET /users/{userId}/locale

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.userLocale+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200

    + Body
    
            {
                "userLocale": {
                    "locale": "en",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/users/1/locale"
                        }
                    ]
                }
            }

## PUT /users/{userId}/locale

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.userLocale+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
        
    + Body
    
            {
                "userLocale": {
                    "locale": "en"
                }
            }

+ Response 200

    + Body
    
            {
                "userLocale": {
                    "locale": "en",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/users/1/locale"
                        }
                    ]
                }
            }

## POST /users/{userId}/introductoryinstructions/disable

Saves the information that user viewed introductory instructions on Web front-end, 
i.e. sets `viewIntroductoryInstructions` of user with id=`userId` to `false`.

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.user+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200

    + Body
    
            {
                "user": {
                    "id": 1,
                    "email": "nedorezov@own.space",
                    "firstName": "Aleksandr",
                    "lastName": "Nedorezov",
                    "displayName": "Aleksandr",
                    "locale": "en",
                    "dailyActivityDigest": true,
                    "status": "ACTIVE",
                    "viewIntroductoryInstructions": false,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/users/1"
                        },
                        {
                            "rel": "profileThumbnail",
                            "href": "/users/1/profileThumbnail"
                        },
                        {
                            "rel": "quota",
                            "href": "/users/1/quota"
                        }
                    ]
                }
            }


# Group Board Elements

Common http codes returned by operations on elements:

+ `200` when sucessfully retrieved or deleted elements
+ `201` when a new element was successfully created
+ `403` returned if the token is expired, invalid or not found
+ `409` when there is a conflict, e.g. position already occupied

## GET /boards/{boardId}/elements

`embeddedLink` link is added for those elements in which file with highest index is a link,
url of which starts with `https://embed.own.space`.

`unviewedFileCount` parameter states how many files in the element user has not seen yet.

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.element+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 (application/vnd.uberblik.elements+json)

    + Body
    
            {
               "elements":[
                  {
                     "id": 1,
                     "sizeX":1,
                     "sizeY":1,
                     "posX":1,
                     "posY":1,
                     "caption":"",
                     "type":"MultiInput",
                     "fileCount":4,
                     "unviewedFileCount": 0,
                     "agentTaskId":null,
                     "_links":[
                        {
                           "rel":"self",
                           "href":"/boards/1/elements/1"
                        },
                        {
                           "rel":"files",
                           "href":"/boards/1/elements/1/files"
                        },
                        {
                           "rel":"thumbnail",
                           "href":"/boards/1/elements/1/thumbnail"
                        },
                        {
                           "rel":"boardThumbnail",
                           "href":"/boards/1/elements/1/boardThumbnail"
                        },
                        {
                           "rel":"masterThumbnail",
                           "href":"/boards/1/elements/1/masterThumbnail"
                        }
                     ]
                  },
                  {
                     "id": 21,
                     "sizeX":1,
                     "sizeY":1,
                     "posX":2,
                     "posY":1,
                     "caption":"",
                     "type":"MultiInput",
                     "fileCount":5,
                     "unviewedFileCount": 1,
                     "agentTaskId":2,
                     "_links":[
                        {
                           "rel":"self",
                           "href":"/boards/1/elements/61"
                        },
                        {
                           "rel":"files",
                           "href":"/boards/1/elements/61/files"
                        },
                        {
                           "rel":"thumbnail",
                           "href":"/boards/1/elements/61/thumbnail"
                        },
                        {
                           "rel":"boardThumbnail",
                           "href":"/boards/1/elements/61/boardThumbnail"
                        },
                        {
                           "rel":"masterThumbnail",
                           "href":"/boards/1/elements/61/masterThumbnail"
                        },
                        {
                           "rel":"agentTask",
                           "href":"/agentdata/61/agenttasks/2"
                        }
                     ]
                  },
                  {
                     "id": 22,
                     "sizeX":1,
                     "sizeY":1,
                     "posX":1,
                     "posY":2,
                     "caption":"",
                     "type":"MultiInput",
                     "fileCount":2,
                     "unviewedFileCount": 0,
                     "agentTaskId":null,
                     "_links":[
                        {
                           "rel":"self",
                           "href":"/boards/1/elements/81"
                        },
                        {
                           "rel":"files",
                           "href":"/boards/1/elements/81/files"
                        },
                        {
                           "rel":"thumbnail",
                           "href":"/boards/1/elements/81/thumbnail"
                        },
                        {
                           "rel":"boardThumbnail",
                           "href":"/boards/1/elements/81/boardThumbnail"
                        },
                        {
                           "rel":"masterThumbnail",
                           "href":"/boards/1/elements/81/masterThumbnail"
                        },
                        {
                           "rel":"embeddedLink",
                           "href":"https://embed.own.space/data/"
                        }
                     ]
                  }
               ],
               "_links":[
                  {
                     "rel":"self",
                     "href":"/boards/1/elements"
                  }
               ]
            }


## POST /boards/{boardId}/elements

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.element+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

    + Body
    
            {
                "element":{
                    "posX":"5",
                    "posY":"5",
                    "sizeX":"2",
                    "sizeY":"2",
                    "type":"MultiInput",
                    "caption":"this is a test element"
                }
            }

+ Response 409 ()

    + Headers 
    
            x-uberblik-error : ElementNotPlaceableAtSpecifiedPosition

+ Response 200 (application/vnd.uberblik.element+json)

    + Body
    
            {
                "element":{
                    "id": 1,
                    "posX":"5",
                    "posY":"5",
                    "sizeX":"2",
                    "sizeY":"2",
                    "type":"MultiInput",
                    "caption":"this is a test element",
                    "fileCount":0,
                    "unviewedFileCount": 0,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/1/elements/361"
                        },
                        {
                            "rel":"files",
                            "href":"/boards/1/elements/361/files"
                        }
                    ]
                }
            }

+ Response 200 (application/vnd.uberblik.element+json)

    + Body            
            
            {
                "element":{
                    "id": 1,
                    "sizeX":2,
                    "sizeY":2,
                    "posX":5,
                    "posY":5,
                    "caption":"this is a test element",
                    "type":"MultiInput",
                    "fileCount":4,
                    "unviewedFileCount": 2,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/1/elements/1"
                        },
                        {
                            "rel":"files",
                            "href":"/boards/1/elements/1/files"
                        },
                        {
                            "rel":"thumbnail",
                            "href":"/boards/1/elements/1/thumbnail"
                        },
                        {
                            "rel":"boardThumbnail",
                            "href":"/boards/1/elements/1/boardThumbnail"
                        },
                        {
                            "rel":"masterThumbnail",
                            "href":"/boards/1/elements/1/masterThumbnail"
                        }
                    ]
                }
            }

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.element+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

    + Body
    
            {
                "element": {
                    "posX":"1", 
                    "posY":"1", 
                    "sizeX":"2", 
                    "sizeY":"2", 
                    "type":"MultiInput",
                    "caption" : "this is a test element"
                }
            }

+ Response 409 ()

    + Headers 
    
            x-uberblik-error : ElementNotPlaceableAtSpecifiedPosition


+ Response 200 (application/vnd.uberblik.element+json)

    + Body            
            
            {
                "element":{
                    "id": 1,
                    "sizeX":2,
                    "sizeY":2,
                    "posX":1,
                    "posY":1,
                    "caption":"",
                    "type":"MultiInput",
                    "fileCount":4,
                    "unviewedFileCount": 0,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/1/elements/1"
                        },
                        {
                            "rel":"files",
                            "href":"/boards/1/elements/1/files"
                        },
                        {
                            "rel":"thumbnail",
                            "href":"/boards/1/elements/1/thumbnail"
                        },
                        {
                            "rel":"boardThumbnail",
                            "href":"/boards/1/elements/1/boardThumbnail"
                        },
                        {
                            "rel":"masterThumbnail",
                            "href":"/boards/1/elements/1/masterThumbnail"
                        }
                    ]
                }
            }

+ Response 200 (application/vnd.uberblik.element+json)

    + Body
    
            {
                "element":{
                    "id": 1,
                    "sizeX":2,
                    "sizeY":2,
                    "posX":1,
                    "posY":1,
                    "caption":"this is a test element",
                    "type":"MultiInput",
                    "fileCount":0,
                    "unviewedFileCount": 0,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/1/elements/361"
                        },
                        {
                            "rel":"files",
                            "href":"/boards/1/elements/361/files"
                        }
                    ]
                }
            }

## GET /boards/{boardId}/elements/{elementId}

`embeddedLink` link is added for those elements in which file with highest index is a link,
url of which starts with `https://embed.own.space`.

`unviewedFileCount` parameter states how many files in the element user has not seen yet.

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.element+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 (application/vnd.uberblik.element+json)

    + Body            
            
            {
                "element":{
                    "id": 1,
                    "sizeX":1,
                    "sizeY":1,
                    "posX":1,
                    "posY":1,
                    "caption":"",
                    "type":"MultiInput",
                    "fileCount":4,
                    "unviewedFileCount": 1,
                    "agentTaskId":21,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/1/elements/1"
                        },
                        {
                            "rel":"files",
                            "href":"/boards/1/elements/1/files"
                        },
                        {
                            "rel":"thumbnail",
                            "href":"/boards/1/elements/1/thumbnail"
                        },
                        {
                            "rel":"boardThumbnail",
                            "href":"/boards/1/elements/1/boardThumbnail"
                        },
                        {
                            "rel":"masterThumbnail",
                            "href":"/boards/1/elements/1/masterThumbnail"
                        },
                        {
                            "rel":"agentTask",
                            "href":"/agentdata/61/agenttasks/21"
                        }
                    ]
                }
            }

+ Response 200 (application/vnd.uberblik.element+json)

    + Body            
            
            {
                "element":{
                    "id": 1,
                    "sizeX":1,
                    "sizeY":1,
                    "posX":1,
                    "posY":1,
                    "caption":"",
                    "type":"MultiInput",
                    "fileCount":4,
                    "unviewedFileCount": 2,
                    "agentTaskId":null,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/1/elements/1"
                        },
                        {
                            "rel":"files",
                            "href":"/boards/1/elements/1/files"
                        },
                        {
                            "rel":"thumbnail",
                            "href":"/boards/1/elements/1/thumbnail"
                        },
                        {
                            "rel":"boardThumbnail",
                            "href":"/boards/1/elements/1/boardThumbnail"
                        },
                        {
                            "rel":"masterThumbnail",
                            "href":"/boards/1/elements/1/masterThumbnail"
                        }
                    ]
                }
            }

+ Response 200 (application/vnd.uberblik.element+json)

    + Body
    
            {
                "element":{
                    "id": 1,
                    "sizeX":2,
                    "sizeY":2,
                    "posX":5,
                    "posY":5,
                    "caption":"this is a test element",
                    "type":"MultiInput",
                    "fileCount":0,
                    "unviewedFileCount": 0,
                    "agentTaskId":null,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/1/elements/361"
                        },
                        {
                            "rel":"files",
                            "href":"/boards/1/elements/361/files"
                        }
                    ]
                }
            }

+ Response 200 (application/vnd.uberblik.element+json)

    + Body

            {
                "element": {
                    "id": 1,
                    "sizeX": 1,
                    "sizeY": 1,
                    "posX": 1,
                    "posY": 2,
                    "caption": "",
                    "type": "MultiInput",
                    "fileCount": 2,
                    "unviewedFileCount": 0,
                    "agentTaskId": null,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/1/elements/81"
                        },
                        {
                            "rel": "files",
                            "href": "/boards/1/elements/81/files"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/1/elements/81/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/1/elements/81/boardThumbnail"
                        },
                        {
                            "rel": "masterThumbnail",
                            "href": "/boards/1/elements/81/masterThumbnail"
                        },
                        {
                            "rel": "embeddedLink",
                            "href": "https://embed.own.space/data/"
                        }
                    ]
                }
            }

## PUT /boards/{boardId}/elements/{elementId}

JSON with any of the fields given in requests body (not necessary all of them), will also be a valid body for this request. Therefore, in the request body, you may only pass those user parameters, which you want to modify.

Note that you should pass `null` as agentTaskId if no agent task is assigned to that element.

If element has no agent task, no "agentTask" link will be returned.

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.element+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

    + Body
    
            {
                "element":{
                    "posX":"5",
                    "posY":"5",
                    "sizeX":"2",
                    "sizeY":"2",
                    "type":"MultiInput",
                    "caption":"this is a test element"
                }
            }

+ Response 409 ()

    + Headers 
    
            x-uberblik-error : ElementNotPlaceableAtSpecifiedPosition
        

+ Response 200 (application/vnd.uberblik.element+json)

    + Body            
            
            {
                "element":{
                    "id": 1,
                    "sizeX":2,
                    "sizeY":2,
                    "posX":5,
                    "posY":5,
                    "caption":"this is a test element",
                    "type":"MultiInput",
                    "fileCount":4,
                    "unviewedFileCount": 0,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/1/elements/1"
                        },
                        {
                            "rel":"files",
                            "href":"/boards/1/elements/1/files"
                        },
                        {
                            "rel":"thumbnail",
                            "href":"/boards/1/elements/1/thumbnail"
                        },
                        {
                            "rel":"boardThumbnail",
                            "href":"/boards/1/elements/1/boardThumbnail"
                        },
                        {
                            "rel":"masterThumbnail",
                            "href":"/boards/1/elements/1/masterThumbnail"
                        }
                    ]
                }
            }

+ Response 200 (application/vnd.uberblik.element+json)

    + Body
    
            {
                "element":{
                    "id": 1,
                    "sizeX":2,
                    "sizeY":2,
                    "posX":5,
                    "posY":5,
                    "caption":"this is a test element",
                    "type":"MultiInput",
                    "fileCount":0,
                    "unviewedFileCount": 0,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/1/elements/361"
                        },
                        {
                            "rel":"files",
                            "href":"/boards/1/elements/361/files"
                        }
                    ]
                }
            }

## DELETE /boards/{boardId}/elements/{elementId}

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.element+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 ()

## GET /boards/{id}/elements/{elementId}/thumbnail

+ Request
    + Headers
    
            Accept: image/jpg, image/png, image/gif, application/pdf

+ Response 200 
    + Headers 

            Content-Length: 346245
            Content-Type: image/jpeg
            
    + Body
    
            gh6f6g346gf3g46r346rr4h9d273hd293hh32...
            
## GET /boards/{id}/elements/{elementId}/boardThumbnail

+ Request
    + Headers
    
            Accept: image/jpg, image/png, image/gif, application/pdf

+ Response 200 
    + Headers 

            Content-Length: 346245
            Content-Type: image/jpeg
            
    + Body
    
            gh6f6g346gf3g46r346rr4h9d273hd293hh32...

## GET /boards/{id}/elements/{elementId}/masterThumbnail

+ Request
    + Headers
    
            Accept: image/jpg, image/png, image/gif, application/pdf

+ Response 200 
    + Headers 

            Content-Length: 346245
            Content-Type: image/jpeg
            
    + Body
    
            gh6f6g346gf3g46r346rr4h9d273hd293hh32...

# Group Element files, thumbnails and previews

### Parameters for Previews

Previews are representations of the original file, optimized for viewing inside the current viewport. In order for the server to 
render the optimal preview, the height of the current viewport is required. 

`viewportHeight` The height of the client viewport in pixels. The width is calculated to retain the original aspect-ratio.

### Response Headers for Previews

Once the client requests a preview from the backend passing the `viewportHeight` parameter, the backend 
calculates 4 values that are returned to the client via the following headers:

`x-uberblik-image-height` The actual height of the image <br>
`x-uberblik-image-width` The actual width of the image<br>
`x-uberblik-viewport-height` The height of the viewport, same as passed viewportHeight parameter<br>
`x-uberblik-viewport-width` The calculated width (according to the image ratio) for the viewport. <br>

With these values, the client can allocate space in the viewport for the image to load, making it 
possible to display a loading indicator with a placeholder that already has the final size.

### File ordering

The files of an element are ordered. The `index` property determines the order of an individual file.
When changing the order of a file with a `PATCH`, the server inserts the file at the provided index 
position and shifts the remaining files accordingly. Index starts at 0.

### URLs stored as Files

The server stores URLs as image in elements. The folowing request describes the addition of an URL as a file in an element. 
The backend should check the url parameter and verify that it is a valid url. If the url is not valid, the server should 
return a non valid HTTP code (400). In all other cases, the server should attempt to obtain a title, description and a list 
of possible thumbnails for the url.  A default thumbnail image should always be available as a selection for the user and 
should be added at the end of the thumbnail image list. If the server fails to get a title or a descriptions, it leaves those 
empty. If the server fails to find a thumbnail for it, it should use the default thumbnail image.

### Charts stored as Files

Possible types of charts are: `BAR`, `LINE`, `PIE`, `SCATTER`, and `RADAR`.

All numeric values in charts can be floating point values, even if in request example integer values are used.

Axis names can be `null`.

Bar chart example:

[![Bar chart](https://s9.postimg.cc/xmmdyp6vj/Bar_Chart.png)](https://s9.postimg.cc/xmmdyp6vj/Bar_Chart.png)

Line chart example:

[![Line chart](https://s9.postimg.cc/59qw89nq7/Line_Chart.png)](https://s9.postimg.cc/59qw89nq7/Line_Chart.png)

Pie chart example:
                                                           
[![Pie chart](https://s9.postimg.cc/u30g8wrb3/Pie_Chart.png)](https://s9.postimg.cc/u30g8wrb3/Pie_Chart.png)

Radar chart example:

[![Radar chart](https://s9.postimg.cc/kigtm1p4f/Radar_Chart.png)](https://s9.postimg.cc/kigtm1p4f/Radar_Chart.png)

Scatter chart example:

[![Scatter chart](https://s9.postimg.cc/7r2nfizwv/Scatter_Chart.png)](https://s9.postimg.cc/7r2nfizwv/Scatter_Chart.png)

### Common http codes returned by operations on files, previews or thumbnails:

+ `200` when sucessfully retrieved, deleted or updated files, previews or thumbnails
+ `201` when a new file or thumbnail was successfully created
+ `400` when reordering a file to a position that does not exist or the height parameter was omitted
+ `403` returned if the token is expired, invalid or not found
+ `409` returned if file upload did not finish completely / successfully
+ `413` returned if file upload failed due to lack of storage space in the board



## POST /boards/{boardId}/elements/{elementId}/files

Note that when uploading html references, fields `title`, `summary`, and `scrapeImagesFromUrl` are not mandatory. 
You can omit them from the request JSON, or use any single one of them, or both both of them.

When `scrapeImagesFromUrl` is `false`, only image from `defaultImageUrl` will serve as a thumbnail, 
images won't be scraped from the web page.

Possible types of charts are: `BAR`, `LINE`, `PIE`, `SCATTER`, and `RADAR`.

For `BAR` and `LINE` charts all series must contain names (names should not be null), 
and names for series must be unique.

For `LINE` charts `tooltip` is not a mandatory field for series data.

You can also exclude any of tooltips fields (`text`, `img`, `url`) from request. 

For `RADAR` chart size(data.indicator)==size(series[i].data.value), 
and charts series.data.value[i]<=data.indicator[i].max.

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.fileCreationResponse+json
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            Content-Type: image/png

    + Body
    
            gh6f6g346gf3g46r346rr4h9d273hd293hh32...


+ Response 201 (application/vnd.uberblik.fileCreationResponse+json)

    + Body
    
            {
                "fileCreationResponse" : 
                { 
                    "name" : "file 01", 
                    "fileType": "application/pdf",
                    "index": 1,
                    "_links":
                    [
                        { "rel" : "self", "href": "/boards/211/elements/6327654/files/9755" },
                        { "rel" : "thumbnail", "href": "/boards/211/elements/6327654/files/9755/thumbnail" },
                        { "rel" : "boardThumbnail", "href": "/boards/211/elements/6327654/files/9755/boardThumbnail" },
                        { "rel" : "preview", "href": "/boards/211/elements/6327654/files/9755/preview" }
                    ]
                }
            }

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.htmlReference+json
            access-token: uywg87gw6gf6g468gf46g4f6g34f4f4
            Content-Type: application/json;charset:UTF-8

    + Body
    
            {
                "htmlReference": {
                    "url": "https://alnedorezov.com",
                    "defaultImageUrl": "defaultImageUrl": "http://www.uberblik.com/assets/defaultHtmlRef.jpg"
                }
            }

+ Response 201 (application/vnd.uberblik.htmlReference+json)

    + Headers 

            x-uberblik-file-index: 23
            x-uberblik-filename: http://www.spiegel.de
    
    + Body
    
            {
                "htmlReference": {
                    "summary": "Software projects management, software development teams management., etc.",
                    "url": "https://alnedorezov.com",
                    "date": "2019-02-26T13:10:58+0000",
                    "thumbs": [
                        "https://alnedorezov.com/images/avatar_2016.jpg",
                        "https://alnedorezov.com/images/icn-facebook.jpg",
                        "https://alnedorezov.com/images/icn-twitter.jpg",
                        "https://alnedorezov.com/images/icn-print.jpg",
                        "https://alnedorezov.com/images/icn-contact.jpg",
                        "https://alnedorezov.com/images/icn-save.jpg",
                        "defaultImageUrl": "http://www.uberblik.com/assets/defaultHtmlRef.jpg"
                    ],
                    "title": "Aleksandr Nedorezov's CV",
                    "titleThumb": "https://alnedorezov.com/images/avatar_2016.jpg",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/243/elements/541/files/10506"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/243/elements/541/files/10506/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/243/elements/541/files/10506/boardThumbnail"
                        },
                        {
                            "rel": "preview",
                            "href": "/boards/243/elements/541/files/10506/preview"
                        },
                        {
                            "rel": "temporaryPreviewLink",
                            "href": "/boards/243/elements/541/files/10506/temporaryPreviewLink"
                        },
                        {
                            "rel": "comments",
                            "href": "/boards/243/elements/541/files/10506/comments"
                        }
                    ]
                }
            }
            
+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.htmlReference+json
            access-token: uywg87gw6gf6g468gf46g4f6g34f4f4
            Content-Type: application/json;charset:UTF-8

    + Body
    
            {
                "htmlReference": {
                    "url": "https://alnedorezov.com",
                    "defaultImageUrl": "http://www.uberblik.com/assets/defaultHtmlRef.jpg",
                    "title": "Aleksandr Nedorezov - Software Engineer",
                    "summary": "Aleksandr Nedorezov's CV"
                }
            }

+ Response 201 (application/vnd.uberblik.htmlReference+json)

    + Headers 

            x-uberblik-file-index: 23
            x-uberblik-filename: http://www.spiegel.de
    
    + Body
    
            {
                "htmlReference": {
                    "summary": "Aleksandr Nedorezov's CV",
                    "url": "https://alnedorezov.com",
                    "date": "2019-02-26T12:55:03+0000",
                    "thumbs": [
                        "https://alnedorezov.com/images/avatar_2016.jpg",
                        "https://alnedorezov.com/images/icn-facebook.jpg",
                        "https://alnedorezov.com/images/icn-twitter.jpg",
                        "https://alnedorezov.com/images/icn-print.jpg",
                        "https://alnedorezov.com/images/icn-contact.jpg",
                        "https://alnedorezov.com/images/icn-save.jpg",
                        "http://www.uberblik.com/assets/defaultHtmlRef.jpg"
                    ],
                    "title": "Aleksandr Nedorezov - Software Engineer",
                    "titleThumb": "https://alnedorezov.com/images/avatar_2016.jpg",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/243/elements/541/files/10503"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/243/elements/541/files/10503/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/243/elements/541/files/10503/boardThumbnail"
                        },
                        {
                            "rel": "preview",
                            "href": "/boards/243/elements/541/files/10503/preview"
                        },
                        {
                            "rel": "temporaryPreviewLink",
                            "href": "/boards/243/elements/541/files/10503/temporaryPreviewLink"
                        },
                        {
                            "rel": "comments",
                            "href": "/boards/243/elements/541/files/10503/comments"
                        }
                    ]
                }
            }

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.htmlReference+json
            access-token: uywg87gw6gf6g468gf46g4f6g34f4f4
            Content-Type: application/json;charset:UTF-8

    + Body
    
            {
                "htmlReference": {
                    "url": "https://alnedorezov.com",
                    "defaultImageUrl": "http://www.uberblik.com/assets/defaultHtmlRef.jpg",
                    "title": "Aleksandr Nedorezov - Software Engineer",
                    "summary": "Aleksandr Nedorezov's CV",
                    "scrapeImagesFromUrl": false
                }
            }

+ Response 201 (application/vnd.uberblik.htmlReference+json)

    + Headers 

            x-uberblik-file-index: 23
            x-uberblik-filename: http://www.spiegel.de
    
    + Body
    
            {
                "htmlReference": {
                    "summary": "Aleksandr Nedorezov's CV",
                    "url": "https://alnedorezov.com",
                    "date": "2019-02-26T12:55:03+0000",
                    "thumbs": [
                        "http://www.uberblik.com/assets/defaultHtmlRef.jpg"
                    ],
                    "title": "Aleksandr Nedorezov - Software Engineer",
                    "titleThumb": "http://www.uberblik.com/assets/defaultHtmlRef.jpg",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/243/elements/541/files/10503"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/243/elements/541/files/10503/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/243/elements/541/files/10503/boardThumbnail"
                        },
                        {
                            "rel": "preview",
                            "href": "/boards/243/elements/541/files/10503/preview"
                        },
                        {
                            "rel": "temporaryPreviewLink",
                            "href": "/boards/243/elements/541/files/10503/temporaryPreviewLink"
                        },
                        {
                            "rel": "comments",
                            "href": "/boards/243/elements/541/files/10503/comments"
                        }
                    ]
                }
            }

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.chart+json
            access-token: uywg87gw6gf6g468gf46g4f6g34f4f4
            Content-Type: application/json;charset:UTF-8

    + Body
    
            {
                "chart":{
                    "title":"BarChart",
                    "type":"BAR",
                    "data":{
                        "series":[
                            {
                                "name":"NAME",
                                "data":[
                                    18203,
                                    23489,
                                    29034,
                                    104970,
                                    131744,
                                    630230
                                ]
                            },
                            {
                                "name":"NAME1",
                                "data":[
                                    182,
                                    289,
                                    234,
                                    10970,
                                    13144,
                                    60230
                                ]
                            }
                        ],
                        "xAxis":{
                            "data":[
                                "123",
                                "asd",
                                "1d2",
                                "d12",
                                "d3",
                                "d1"
                            ],
                            "name":"123"
                        },
                        "yAxis":{
                            "name":null
                        }
                    }
                }
            }

+ Response 201 (application/vnd.uberblik.chart+json; charset=utf-8)

    + Headers 

            x-uberblik-file-index: 23
            x-uberblik-filename: BarChart
    
    + Body
    
            {
                "chart": {
                    "title": "BarChart",
                    "data": {
                        "series": [
                            {
                                "name": "NAME",
                                "data": [
                                    18203,
                                    23489,
                                    29034,
                                    104970,
                                    131744,
                                    630230
                                ]
                            },
                            {
                                "name": "NAME1",
                                "data": [
                                    182,
                                    289,
                                    234,
                                    10970,
                                    13144,
                                    60230
                                ]
                            }
                        ],
                        "xAxis": {
                            "data": [
                                "123",
                                "asd",
                                "1d2",
                                "d12",
                                "d3",
                                "d1"
                            ],
                            "name": "123"
                        },
                        "yAxis": {
                            "name": null
                        }
                    },
                    "type": "BAR",
                    "fileId": 681,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/1/elements/61/files/681"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/1/elements/61/files/681/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/1/elements/61/files/681/boardThumbnail"
                        },
                        {
                            "rel": "preview",
                            "href": "/boards/1/elements/61/files/681/preview"
                        },
                        {
                            "rel": "downloadLink",
                            "href": "/boards/1/elements/61/files/681/downloadLink"
                        },
                        {
                            "rel": "temporaryPreviewLink",
                            "href": "/boards/1/elements/61/files/681/temporaryPreviewLink"
                        },
                        {
                            "rel": "comments",
                            "href": "/boards/1/elements/61/files/681/comments"
                        }
                    ]
                }
            }

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.chart+json
            access-token: uywg87gw6gf6g468gf46g4f6g34f4f4
            Content-Type: application/json;charset:UTF-8

    + Body
    
            {
              "chart": {
                "title": "LineChart",
                "type": "LINE",
                "data": {
                  "series": [
                    {
                      "disabled": true,
                      "name": "NAME",
                      "data": [
                        {
                          "value": 820,
                          "tooltip": {
                            "text": "This is text. It is very interesting, and was written very beautifully.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                            "url": "https://alnedorezov.com"
                          }
                        },
                        {
                          "value": 244,
                          "tooltip": {
                            "text": "This is text 2. It is very interesting, and was written very beautifully.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                            "url": null
                          }
                        },
                        {
                          "value": 2432,
                          "tooltip": null
                        },
                        {
                          "value": 456,
                          "tooltip": null
                        },
                        {
                          "value": 896,
                          "tooltip": {
                            "text": null,
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        },
                        {
                          "value": 8532,
                          "tooltip": {
                            "text": "This is text 6. It is very interesting, and was written very beautifully.",
                            "img": null
                          }
                        }
                      ]
                    },
                    {
                      "name": "NAME1",
                      "data": [
                        {
                          "value": 4,
                          "tooltip": {
                            "text": "This is text. It is very interesting, and was written very beautifully.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        },
                        {
                          "value": 256
                        },
                        {
                          "value": 2466,
                          "tooltip": {
                            "text": "This is text 3. It is very interesting, and was written very beautifully.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        },
                        {
                          "value": 346,
                          "tooltip": {
                            "text": "This is text 4. It is very interesting, and was written very beautifully.",
                            "img": ""
                          }
                        },
                        {
                          "value": 8742,
                          "tooltip": {
                            "text": "Ururu. Kokoko.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        },
                        {
                          "value": 32432,
                          "tooltip": {
                            "text": "This is text 6. It is very interesting, and was written very beautifully.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        }
                      ]
                    },
                    {
                      "disabled": null,
                      "name": "NAME1",
                      "data": [
                        {
                          "value": 4,
                          "tooltip": {
                            "text": null,
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        },
                        {
                          "value": 256,
                          "tooltip": {
                            "text": "This is text 2. It is very interesting, and was written very beautifully.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        },
                        {
                          "value": 2466,
                          "tooltip": {
                            "text": "This is text 3. It is very interesting, and was written very beautifully.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        },
                        {
                          "value": 346,
                          "tooltip": {
                            "text": "This is text 4. It is very interesting, and was written very beautifully.",
                            "img": ""
                          }
                        },
                        {
                          "value": 8742,
                          "tooltip": {
                            "text": "",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        },
                        {
                          "value": 32432,
                          "tooltip": {
                            "text": "This is text 6. It is very interesting, and was written very beautifully.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                            "url": ""
                          }
                        }
                      ]
                    }
                  ],
                  "xAxis": {
                    "data": [
                      "123",
                      "asd",
                      "1d2",
                      "d12",
                      "d3",
                      "d1"
                    ],
                    "name": "123"
                  },
                  "yAxis": {
                    "name": null
                  }
                }
              }
            }

+ Response 201 (application/vnd.uberblik.chart+json; charset=utf-8)

    + Headers 

            x-uberblik-file-index: 31
            x-uberblik-filename: LineChart
    
    + Body
    
            {
                "chart": {
                    "title": "LineChart",
                    "data": {
                        "series": [
                            {
                                "name": "NAME",
                                "data": [
                                    {
                                        "value": 820,
                                        "tooltip": {
                                            "text": "This is text. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": "https://alnedorezov.com"
                                        }
                                    },
                                    {
                                        "value": 244,
                                        "tooltip": {
                                            "text": "This is text 2. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 2432,
                                        "tooltip": null
                                    },
                                    {
                                        "value": 456,
                                        "tooltip": null
                                    },
                                    {
                                        "value": 896,
                                        "tooltip": {
                                            "text": null,
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 8532,
                                        "tooltip": {
                                            "text": "This is text 6. It is very interesting, and was written very beautifully.",
                                            "img": null,
                                            "url": null
                                        }
                                    }
                                ],
                                "disabled": true
                            },
                            {
                                "name": "NAME1",
                                "data": [
                                    {
                                        "value": 4,
                                        "tooltip": {
                                            "text": "This is text. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 256,
                                        "tooltip": null
                                    },
                                    {
                                        "value": 2466,
                                        "tooltip": {
                                            "text": "This is text 3. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 346,
                                        "tooltip": {
                                            "text": "This is text 4. It is very interesting, and was written very beautifully.",
                                            "img": "",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 8742,
                                        "tooltip": {
                                            "text": "Ururu. Kokoko.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 32432,
                                        "tooltip": {
                                            "text": "This is text 6. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    }
                                ],
                                "disabled": false
                            },
                            {
                                "name": "NAME1",
                                "data": [
                                    {
                                        "value": 4,
                                        "tooltip": {
                                            "text": null,
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 256,
                                        "tooltip": {
                                            "text": "This is text 2. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 2466,
                                        "tooltip": {
                                            "text": "This is text 3. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 346,
                                        "tooltip": {
                                            "text": "This is text 4. It is very interesting, and was written very beautifully.",
                                            "img": "",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 8742,
                                        "tooltip": {
                                            "text": "",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 32432,
                                        "tooltip": {
                                            "text": "This is text 6. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": ""
                                        }
                                    }
                                ],
                                "disabled": false
                            }
                        ],
                        "xAxis": {
                            "data": [
                                "123",
                                "asd",
                                "1d2",
                                "d12",
                                "d3",
                                "d1"
                            ],
                            "name": "123"
                        },
                        "yAxis": {
                            "name": null
                        }
                    },
                    "type": "LINE",
                    "fileId": 1261,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/1/elements/61/files/1261"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/1/elements/61/files/1261/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/1/elements/61/files/1261/boardThumbnail"
                        },
                        {
                            "rel": "preview",
                            "href": "/boards/1/elements/61/files/1261/preview"
                        },
                        {
                            "rel": "downloadLink",
                            "href": "/boards/1/elements/61/files/1261/downloadLink"
                        },
                        {
                            "rel": "temporaryPreviewLink",
                            "href": "/boards/1/elements/61/files/1261/temporaryPreviewLink"
                        },
                        {
                            "rel": "comments",
                            "href": "/boards/1/elements/61/files/1261/comments"
                        }
                    ]
                }
            }

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.chart+json;charset=UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            Content-Type: application/json;charset:UTF-8
                        
    + Body
    
            {
                "chart":{
                    "title":"PieChart",
                    "type":"PIE",
                    "data":{
                        "series":[
                            {
                                "name":"Name",
                                "data":[
                                    {
                                        "value":335,
                                        "name":"12345"
                                    },
                                    {
                                        "value":310,
                                        "name":"abvgdeika"
                                    },
                                    {
                                        "value":234,
                                        "name":"OLOLO"
                                    },
                                    {
                                        "value":135,
                                        "name":"Vulcanos"
                                    },
                                    {
                                        "value":1548,
                                        "name":"Carrots"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }

+ Response 201 (application/vnd.uberblik.chart+json; charset=utf-8)

    + Headers 

            x-uberblik-file-index: 24
            x-uberblik-filename: PieChart
            
    + Body
    
            {
                "chart":{
                    "title":"PieChart",
                    "data":{
                        "series":[
                            {
                                "name":"Name",
                                "data":[
                                    {
                                        "value":335,
                                        "name":"12345"
                                    },
                                    {
                                        "value":310,
                                        "name":"abvgdeika"
                                    },
                                    {
                                        "value":234,
                                        "name":"OLOLO"
                                    },
                                    {
                                        "value":135,
                                        "name":"Vulcanos"
                                    },
                                    {
                                        "value":1548,
                                        "name":"Carrots"
                                    }
                                ]
                            }
                        ]
                    },
                    "type":"PIE",
                    "fileId":483,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/243/elements/472/files/483"
                        },
                        {
                            "rel":"thumbnail",
                            "href":"/boards/243/elements/472/files/483/thumbnail"
                        },
                        {
                            "rel":"boardThumbnail",
                            "href":"/boards/243/elements/472/files/483/boardThumbnail"
                        },
                        {
                            "rel":"preview",
                            "href":"/boards/243/elements/472/files/483/preview"
                        },
                        {
                            "rel":"downloadLink",
                            "href":"/boards/243/elements/472/files/483/downloadLink"
                        },
                        {
                            "rel":"temporaryPreviewLink",
                            "href":"/boards/243/elements/472/files/483/temporaryPreviewLink"
                        },
                        {
                            "rel":"comments",
                            "href":"/boards/243/elements/472/files/483/comments"
                        }
                    ]
                }
            }

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.chart+json;charset=UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            Content-Type: application/json;charset:UTF-8
                        
    + Body
    
            {
                "chart":{
                    "title":"RadarChart",
                    "type":"RADAR",
                    "data":{
                        "indicator":[
                            {
                                "name":"销售（sales）",
                                "max":6500
                            },
                            {
                                "name":"管理（Administration）",
                                "max":16000
                            },
                            {
                                "name":"信息技术（Information Techology）",
                                "max":30000
                            },
                            {
                                "name":"客服（Customer Support）",
                                "max":38000
                            },
                            {
                                "name":"研发（Development）",
                                "max":52000
                            },
                            {
                                "name":"市场（Marketing）",
                                "max":25000
                            }
                        ],
                        "series":[
                            {
                                "name":"预算 vs 开销（Budget vs spending）",
                                "data":[
                                    {
                                        "value":[
                                            4300,
                                            10000,
                                            28000,
                                            35000,
                                            50000,
                                            19000
                                        ],
                                        "name":"预算分配（Allocated Budget）"
                                    },
                                    {
                                        "value":[
                                            5000,
                                            14000,
                                            28000,
                                            31000,
                                            42000,
                                            21000
                                        ],
                                        "name":"实际开销（Actual Spending）"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }

+ Response 201 (application/vnd.uberblik.chart+json; charset=utf-8)

    + Headers 

            x-uberblik-file-index: 25
            x-uberblik-filename: RadarChart
            
    + Body
    
            {
                "chart":{
                    "title":"RadarChart",
                    "data":{
                        "indicator":[
                            {
                                "name":"销售（sales）",
                                "max":6500
                            },
                            {
                                "name":"管理（Administration）",
                                "max":16000
                            },
                            {
                                "name":"信息技术（Information Techology）",
                                "max":30000
                            },
                            {
                                "name":"客服（Customer Support）",
                                "max":38000
                            },
                            {
                                "name":"研发（Development）",
                                "max":52000
                            },
                            {
                                "name":"市场（Marketing）",
                                "max":25000
                            }
                        ],
                        "series":[
                            {
                                "name":"预算 vs 开销（Budget vs spending）",
                                "data":[
                                    {
                                        "value":[
                                            4300,
                                            10000,
                                            28000,
                                            35000,
                                            50000,
                                            19000
                                        ],
                                        "name":"预算分配（Allocated Budget）"
                                    },
                                    {
                                        "value":[
                                            5000,
                                            14000,
                                            28000,
                                            31000,
                                            42000,
                                            21000
                                        ],
                                        "name":"实际开销（Actual Spending）"
                                    }
                                ]
                            }
                        ]
                    },
                    "type":"RADAR",
                    "fileId":523,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/1/elements/1/files/523"
                        },
                        {
                            "rel":"thumbnail",
                            "href":"/boards/1/elements/1/files/523/thumbnail"
                        },
                        {
                            "rel":"boardThumbnail",
                            "href":"/boards/1/elements/1/files/523/boardThumbnail"
                        },
                        {
                            "rel":"preview",
                            "href":"/boards/1/elements/1/files/523/preview"
                        },
                        {
                            "rel":"downloadLink",
                            "href":"/boards/1/elements/1/files/523/downloadLink"
                        },
                        {
                            "rel":"temporaryPreviewLink",
                            "href":"/boards/1/elements/1/files/523/temporaryPreviewLink"
                        },
                        {
                            "rel":"comments",
                            "href":"/boards/1/elements/1/files/523/comments"
                        }
                    ]
                }
            }

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.chart+json;charset=UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            Content-Type: application/json;charset:UTF-8
                        
    + Body
    
            {
                "chart":{
                    "title":"ScatterChart",
                    "type":"SCATTER",
                    "data":{
                        "xAxis":{
                            "name":"123"
                        },
                        "yAxis":{
                            "name":null
                        },
                        "series":[
                            {
                                "name":"scatter 1",
                                "data":[
                                    [
                                        10.0,
                                        8.04
                                    ],
                                    [
                                        8.0,
                                        6.95
                                    ],
                                    [
                                        13.0,
                                        7.58
                                    ],
                                    [
                                        9.0,
                                        8.81
                                    ],
                                    [
                                        11.0,
                                        8.33
                                    ],
                                    [
                                        14.0,
                                        9.96
                                    ],
                                    [
                                        6.0,
                                        7.24
                                    ],
                                    [
                                        4.0,
                                        4.26
                                    ],
                                    [
                                        12.0,
                                        10.84
                                    ],
                                    [
                                        7.0,
                                        4.82
                                    ],
                                    [
                                        5.0,
                                        5.68
                                    ]
                                ]
                            },
                            {
                                "name":"scatter 2",
                                "data":[
                                    [
                                        10.0,
                                        8.04
                                    ],
                                    [
                                        8.0,
                                        6.95
                                    ],
                                    [
                                        13.0,
                                        7.58
                                    ],
                                    [
                                        9.0,
                                        5.81
                                    ],
                                    [
                                        4.0,
                                        4.26
                                    ],
                                    [
                                        12.0,
                                        10.84
                                    ],
                                    [
                                        7.0,
                                        4.82
                                    ],
                                    [
                                        5.0,
                                        5.68
                                    ]
                                ]
                            }
                        ]
                    }
                }
            }
    
+ Response 201 (application/vnd.uberblik.chart+json; charset=utf-8)

    + Headers 

            x-uberblik-file-index: 26
            x-uberblik-filename: ScatterChart
            
    + Body
    
            {
                "chart": {
                    "title": "ScatterChart",
                    "data": {
                        "xAxis": {
                            "name": "123"
                        },
                        "yAxis": {
                            "name": null
                        },
                        "series": [
                            {
                                "name": "scatter 1",
                                "data": [
                                    [
                                        10,
                                        8.04
                                    ],
                                    [
                                        8,
                                        6.95
                                    ],
                                    [
                                        13,
                                        7.58
                                    ],
                                    [
                                        9,
                                        8.81
                                    ],
                                    [
                                        11,
                                        8.33
                                    ],
                                    [
                                        14,
                                        9.96
                                    ],
                                    [
                                        6,
                                        7.24
                                    ],
                                    [
                                        4,
                                        4.26
                                    ],
                                    [
                                        12,
                                        10.84
                                    ],
                                    [
                                        7,
                                        4.82
                                    ],
                                    [
                                        5,
                                        5.68
                                    ]
                                ]
                            },
                            {
                                "name": "scatter 2",
                                "data": [
                                    [
                                        10,
                                        8.04
                                    ],
                                    [
                                        8,
                                        6.95
                                    ],
                                    [
                                        13,
                                        7.58
                                    ],
                                    [
                                        9,
                                        5.81
                                    ],
                                    [
                                        4,
                                        4.26
                                    ],
                                    [
                                        12,
                                        10.84
                                    ],
                                    [
                                        7,
                                        4.82
                                    ],
                                    [
                                        5,
                                        5.68
                                    ]
                                ]
                            }
                        ]
                    },
                    "type": "SCATTER",
                    "fileId": 686,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/1/elements/61/files/686"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/1/elements/61/files/686/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/1/elements/61/files/686/boardThumbnail"
                        },
                        {
                            "rel": "preview",
                            "href": "/boards/1/elements/61/files/686/preview"
                        },
                        {
                            "rel": "downloadLink",
                            "href": "/boards/1/elements/61/files/686/downloadLink"
                        },
                        {
                            "rel": "temporaryPreviewLink",
                            "href": "/boards/1/elements/61/files/686/temporaryPreviewLink"
                        },
                        {
                            "rel": "comments",
                            "href": "/boards/1/elements/61/files/686/comments"
                        }
                    ]
                }
            }

## GET /boards/{boardId}/elements/{elementId}/files

`viewed` parameter states whether user viewed file already or not.

This request marks all files in element with id=`elementId` as viewed for the user who sent the request, 
while returning their previous `viewed` values.

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.files+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 (application/json)

    + Body
    
            {
                "files":[
                    {
                        "name":"goodreads_quotes_export.csv.zip",
                        "fileType":"application/zip",
                        "index":4,
                        "viewed": false,
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/boards/1/elements/462/files/450"
                            },
                            {
                                "rel":"thumbnail",
                                "href":"/boards/1/elements/462/files/450/thumbnail"
                            },
                            {
                                "rel":"boardThumbnail",
                                "href":"/boards/1/elements/462/files/450/boardThumbnail"
                            },
                            {
                                "rel":"preview",
                                "href":"/boards/1/elements/462/files/450/preview"
                            },
                            {
                                "rel":"downloadLink",
                                "href":"/boards/1/elements/462/files/450/downloadLink"
                            },
                            {
                                "rel":"temporaryPreviewLink",
                                "href":"/boards/1/elements/462/files/450/temporaryPreviewLink"
                            },
                            {
                                "rel":"comments",
                                "href":"/boards/1/elements/462/files/450/comments"
                            }
                        ]
                    },
                    {
                        "name":"manual.pdf",
                        "fileType":"application/pdf",
                        "index":3,
                        "viewed": true,
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/boards/1/elements/462/files/449"
                            },
                            {
                                "rel":"thumbnail",
                                "href":"/boards/1/elements/462/files/449/thumbnail"
                            },
                            {
                                "rel":"boardThumbnail",
                                "href":"/boards/1/elements/462/files/449/boardThumbnail"
                            },
                            {
                                "rel":"preview",
                                "href":"/boards/1/elements/462/files/449/preview"
                            },
                            {
                                "rel":"downloadLink",
                                "href":"/boards/1/elements/462/files/449/downloadLink"
                            },
                            {
                                "rel":"temporaryPreviewLink",
                                "href":"/boards/1/elements/462/files/449/temporaryPreviewLink"
                            },
                            {
                                "rel":"comments",
                                "href":"/boards/1/elements/462/files/449/comments"
                            }
                        ]
                    },
                    {
                        "name":"30425083_1676182275770875_2512253027788886265_o.jpg",
                        "fileType":"image/jpeg",
                        "index":2,
                        "viewed": true,
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/boards/1/elements/462/files/448"
                            },
                            {
                                "rel":"thumbnail",
                                "href":"/boards/1/elements/462/files/448/thumbnail"
                            },
                            {
                                "rel":"boardThumbnail",
                                "href":"/boards/1/elements/462/files/448/boardThumbnail"
                            },
                            {
                                "rel":"preview",
                                "href":"/boards/1/elements/462/files/448/preview"
                            },
                            {
                                "rel":"downloadLink",
                                "href":"/boards/1/elements/462/files/448/downloadLink"
                            },
                            {
                                "rel":"temporaryPreviewLink",
                                "href":"/boards/1/elements/462/files/448/temporaryPreviewLink"
                            },
                            {
                                "rel":"comments",
                                "href":"/boards/1/elements/462/files/448/comments"
                            }
                        ]
                    },
                    {
                        "name":"BarChart",
                        "fileType":"application/vnd.uberblik.chart+json",
                        "index":1,
                        "viewed": true,
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/boards/1/elements/462/files/444"
                            },
                            {
                                "rel":"thumbnail",
                                "href":"/boards/1/elements/462/files/444/thumbnail"
                            },
                            {
                                "rel":"boardThumbnail",
                                "href":"/boards/1/elements/462/files/444/boardThumbnail"
                            },
                            {
                                "rel":"preview",
                                "href":"/boards/1/elements/462/files/444/preview"
                            },
                            {
                                "rel":"downloadLink",
                                "href":"/boards/1/elements/462/files/444/downloadLink"
                            },
                            {
                                "rel":"temporaryPreviewLink",
                                "href":"/boards/1/elements/462/files/444/temporaryPreviewLink"
                            },
                            {
                                "rel":"comments",
                                "href":"/boards/1/elements/462/files/444/comments"
                            }
                        ]
                    },
                    {
                        "name":"http://www.mi.com/us/",
                        "fileType":"application/vnd.uberblik.htmlReference",
                        "index":0,
                        "viewed": true,
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/boards/1/elements/462/files/443"
                            },
                            {
                                "rel":"thumbnail",
                                "href":"/boards/1/elements/462/files/443/thumbnail"
                            },
                            {
                                "rel":"boardThumbnail",
                                "href":"/boards/1/elements/462/files/443/boardThumbnail"
                            },
                            {
                                "rel":"preview",
                                "href":"/boards/1/elements/462/files/443/preview"
                            },
                            {
                                "rel":"temporaryPreviewLink",
                                "href":"/boards/1/elements/462/files/443/temporaryPreviewLink"
                            },
                            {
                                "rel":"comments",
                                "href":"/boards/1/elements/462/files/443/comments"
                            }
                        ]
                    }
                ],
                "_links":[
                    {
                        "rel":"self",
                        "href":"/boards/1/elements/462/files"
                    }
                ]
            }

## PATCH /boards/{boardId}/elements/{elementId}/files

This request marks all files in element with id=`elementId` as viewed for the user who sent the request.

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.files+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 ()

## GET /boards/{boardId}/elements/{elementId}/files/count

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.filesCount+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 (application/json)

    + Body
    
            {
                "filesCount":1
            }

## POST /boards/{boardId}/elements/{elementId}/files/{fileId}/downloadLink

            This resource provides a way to download an asset without following the signing process. It is used for streaming assets such
            as video or audio files, or for download in browswers that don't support URS.
+ Request
    + Headers
    
            Accept: application/vnd.uberblik.downloadLink+json;charset=UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 201

    + Headers 

            Content-Type: application/vnd.uberblik.downloadLink+json;charset=UTF-8
            
    + Body
    
            {
                "downloadLink" : {
                    "url" : "y2621362rgxfcbfx3fni13mzo3gfyn/businessPlan.pdf?token=6t2r63t4rt673g6737fghq7hcbghfhjsg6g4ux2sw28,
                }
            }
    
## HEAD /boards/{boardId}/elements/{elementId}/files/{fileId}

+ Response 200
    + Headers 

            Content-Size: 346272345
            x-uberblik-file-index: 1
            x-uberblik-filename: beautifulPicture.jpg
            Content-Type: image/jpeg
            
+ Response 200
    + Headers 

            Content-Size: 346272345
            x-uberblik-file-index: 23
            x-uberblik-filename: http://www.mi.com/ru/
            Content-Type: application/vnd.uberblik.htmlReference
            
## GET /boards/{boardId}/elements/{elementId}/files/{fileId}

+ Request
    + Headers
    
            Accept: image/jpg, image/png, image/gif, application/pdf
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 
    + Headers 

            Content-Size: 346272345
            Content-Type: image/jpeg
            
    + Body
    
            gh6f6g346gf3g46r346rr4h9d273hd293hh32...
      

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.htmlReference+json;charset=UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 
    + Headers 

            Content-Size: 345
            Content-Type: application/vnd.uberblik.htmlReference+json;charset=UTF-8
            
    + Body
    
            {
                "htmlReference": {
                    "summary": "Aleksandr Nedorezov's CV",
                    "url": "https://alnedorezov.com",
                    "date": "2019-02-26T12:55:03+0000",
                    "thumbs": [
                        "https://alnedorezov.com/images/avatar_2016.jpg",
                        "https://alnedorezov.com/images/icn-facebook.jpg",
                        "https://alnedorezov.com/images/icn-twitter.jpg",
                        "https://alnedorezov.com/images/icn-print.jpg",
                        "https://alnedorezov.com/images/icn-contact.jpg",
                        "https://alnedorezov.com/images/icn-save.jpg"
                    ],
                    "title": "Aleksandr Nedorezov's CV",
                    "titleThumb": "https://alnedorezov.com/images/avatar_2016.jpg",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/243/elements/541/files/10503"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/243/elements/541/files/10503/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/243/elements/541/files/10503/boardThumbnail"
                        },
                        {
                            "rel": "preview",
                            "href": "/boards/243/elements/541/files/10503/preview"
                        },
                        {
                            "rel": "temporaryPreviewLink",
                            "href": "/boards/243/elements/541/files/10503/temporaryPreviewLink"
                        },
                        {
                            "rel": "comments",
                            "href": "/boards/243/elements/541/files/10503/comments"
                        }
                    ]
                }
            }
            
+ Request
    + Headers
    
            Accept: application/vnd.uberblik.chart+json;charset=UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 
    + Headers 

            Content-Length: 781
            Content-Type: application/vnd.uberblik.chart+json;charset=UTF-8
            
    + Body
    
            {
                "chart": {
                    "title": "BarChart",
                    "data": {
                        "series": [
                            {
                                "name": "NAME",
                                "data": [
                                    18203,
                                    23489,
                                    29034,
                                    104970,
                                    131744,
                                    630230
                                ]
                            },
                            {
                                "name": "NAME1",
                                "data": [
                                    182,
                                    289,
                                    234,
                                    10970,
                                    13144,
                                    60230
                                ]
                            }
                        ],
                        "xAxis": {
                            "data": [
                                "123",
                                "asd",
                                "1d2",
                                "d12",
                                "d3",
                                "d1"
                            ],
                            "name": "123"
                        },
                        "yAxis": {
                            "name": null
                        }
                    },
                    "type": "BAR",
                    "fileId": 681,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/1/elements/61/files/681"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/1/elements/61/files/681/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/1/elements/61/files/681/boardThumbnail"
                        },
                        {
                            "rel": "preview",
                            "href": "/boards/1/elements/61/files/681/preview"
                        },
                        {
                            "rel": "downloadLink",
                            "href": "/boards/1/elements/61/files/681/downloadLink"
                        },
                        {
                            "rel": "temporaryPreviewLink",
                            "href": "/boards/1/elements/61/files/681/temporaryPreviewLink"
                        },
                        {
                            "rel": "comments",
                            "href": "/boards/1/elements/61/files/681/comments"
                        }
                    ]
                }
            }

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.chart+json;charset=UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 
    + Headers 

            Content-Length: 781
            Content-Type: application/vnd.uberblik.chart+json;charset=UTF-8
            
    + Body
    
            {
                "chart": {
                    "title": "LineChart",
                    "data": {
                        "series": [
                            {
                                "name": "NAME",
                                "data": [
                                    {
                                        "value": 820,
                                        "tooltip": {
                                            "text": "This is text. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": "https://alnedorezov.com"
                                        }
                                    },
                                    {
                                        "value": 244,
                                        "tooltip": {
                                            "text": "This is text 2. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 2432,
                                        "tooltip": null
                                    },
                                    {
                                        "value": 456,
                                        "tooltip": null
                                    },
                                    {
                                        "value": 896,
                                        "tooltip": {
                                            "text": null,
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 8532,
                                        "tooltip": {
                                            "text": "This is text 6. It is very interesting, and was written very beautifully.",
                                            "img": null,
                                            "url": null
                                        }
                                    }
                                ],
                                "disabled": true
                            },
                            {
                                "name": "NAME1",
                                "data": [
                                    {
                                        "value": 4,
                                        "tooltip": {
                                            "text": "This is text. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 256,
                                        "tooltip": null
                                    },
                                    {
                                        "value": 2466,
                                        "tooltip": {
                                            "text": "This is text 3. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 346,
                                        "tooltip": {
                                            "text": "This is text 4. It is very interesting, and was written very beautifully.",
                                            "img": "",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 8742,
                                        "tooltip": {
                                            "text": "Ururu. Kokoko.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 32432,
                                        "tooltip": {
                                            "text": "This is text 6. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    }
                                ],
                                "disabled": false
                            },
                            {
                                "name": "NAME1",
                                "data": [
                                    {
                                        "value": 4,
                                        "tooltip": {
                                            "text": null,
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 256,
                                        "tooltip": {
                                            "text": "This is text 2. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 2466,
                                        "tooltip": {
                                            "text": "This is text 3. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 346,
                                        "tooltip": {
                                            "text": "This is text 4. It is very interesting, and was written very beautifully.",
                                            "img": "",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 8742,
                                        "tooltip": {
                                            "text": "",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 32432,
                                        "tooltip": {
                                            "text": "This is text 6. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": ""
                                        }
                                    }
                                ],
                                "disabled": false
                            }
                        ],
                        "xAxis": {
                            "data": [
                                "123",
                                "asd",
                                "1d2",
                                "d12",
                                "d3",
                                "d1"
                            ],
                            "name": "123"
                        },
                        "yAxis": {
                            "name": null
                        }
                    },
                    "type": "LINE",
                    "fileId": 1261,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/1/elements/61/files/1261"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/1/elements/61/files/1261/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/1/elements/61/files/1261/boardThumbnail"
                        },
                        {
                            "rel": "preview",
                            "href": "/boards/1/elements/61/files/1261/preview"
                        },
                        {
                            "rel": "downloadLink",
                            "href": "/boards/1/elements/61/files/1261/downloadLink"
                        },
                        {
                            "rel": "temporaryPreviewLink",
                            "href": "/boards/1/elements/61/files/1261/temporaryPreviewLink"
                        },
                        {
                            "rel": "comments",
                            "href": "/boards/1/elements/61/files/1261/comments"
                        }
                    ]
                }
            }

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.chart+json;charset=UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 
    + Headers 

            Content-Length: 767
            Content-Type: application/vnd.uberblik.chart+json;charset=UTF-8
            
    + Body
    
            {
                "chart":{
                    "title":"PieChart",
                    "data":{
                        "series":[
                            {
                                "name":"Name",
                                "data":[
                                    {
                                        "value":335,
                                        "name":"12345"
                                    },
                                    {
                                        "value":310,
                                        "name":"abvgdeika"
                                    },
                                    {
                                        "value":234,
                                        "name":"OLOLO"
                                    },
                                    {
                                        "value":135,
                                        "name":"Vulcanos"
                                    },
                                    {
                                        "value":1548,
                                        "name":"Carrots"
                                    }
                                ]
                            }
                        ]
                    },
                    "type":"PIE",
                    "fileId":483,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/243/elements/472/files/483"
                        },
                        {
                            "rel":"thumbnail",
                            "href":"/boards/243/elements/472/files/483/thumbnail"
                        },
                        {
                            "rel":"boardThumbnail",
                            "href":"/boards/243/elements/472/files/483/boardThumbnail"
                        },
                        {
                            "rel":"preview",
                            "href":"/boards/243/elements/472/files/483/preview"
                        },
                        {
                            "rel":"downloadLink",
                            "href":"/boards/243/elements/472/files/483/downloadLink"
                        },
                        {
                            "rel":"temporaryPreviewLink",
                            "href":"/boards/243/elements/472/files/483/temporaryPreviewLink"
                        },
                        {
                            "rel":"comments",
                            "href":"/boards/243/elements/472/files/483/comments"
                        }
                    ]
                }
            }

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.chart+json;charset=UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 
    + Headers 

            Content-Length: 1149
            Content-Type: application/vnd.uberblik.chart+json;charset=UTF-8
            
    + Body
    
            {
                "chart":{
                    "title":"RadarChart",
                    "data":{
                        "indicator":[
                            {
                                "name":"销售（sales）",
                                "max":6500
                            },
                            {
                                "name":"管理（Administration）",
                                "max":16000
                            },
                            {
                                "name":"信息技术（Information Techology）",
                                "max":30000
                            },
                            {
                                "name":"客服（Customer Support）",
                                "max":38000
                            },
                            {
                                "name":"研发（Development）",
                                "max":52000
                            },
                            {
                                "name":"市场（Marketing）",
                                "max":25000
                            }
                        ],
                        "series":[
                            {
                                "name":"预算 vs 开销（Budget vs spending）",
                                "data":[
                                    {
                                        "value":[
                                            4300,
                                            10000,
                                            28000,
                                            35000,
                                            50000,
                                            19000
                                        ],
                                        "name":"预算分配（Allocated Budget）"
                                    },
                                    {
                                        "value":[
                                            5000,
                                            14000,
                                            28000,
                                            31000,
                                            42000,
                                            21000
                                        ],
                                        "name":"实际开销（Actual Spending）"
                                    }
                                ]
                            }
                        ]
                    },
                    "type":"RADAR",
                    "fileId":523,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/1/elements/1/files/523"
                        },
                        {
                            "rel":"thumbnail",
                            "href":"/boards/1/elements/1/files/523/thumbnail"
                        },
                        {
                            "rel":"boardThumbnail",
                            "href":"/boards/1/elements/1/files/523/boardThumbnail"
                        },
                        {
                            "rel":"preview",
                            "href":"/boards/1/elements/1/files/523/preview"
                        },
                        {
                            "rel":"downloadLink",
                            "href":"/boards/1/elements/1/files/523/downloadLink"
                        },
                        {
                            "rel":"temporaryPreviewLink",
                            "href":"/boards/1/elements/1/files/523/temporaryPreviewLink"
                        },
                        {
                            "rel":"comments",
                            "href":"/boards/1/elements/1/files/523/comments"
                        }
                    ]
                }
            }

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.chart+json;charset=UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 
    + Headers 

            Content-Length: 881
            Content-Type: application/vnd.uberblik.chart+json;charset=UTF-8
            
    + Body
    
            {
                "chart": {
                    "title": "ScatterChart",
                    "data": {
                        "xAxis": {
                            "name": "123"
                        },
                        "yAxis": {
                            "name": null
                        },
                        "series": [
                            {
                                "name": "scatter 1",
                                "data": [
                                    [
                                        10,
                                        8.04
                                    ],
                                    [
                                        8,
                                        6.95
                                    ],
                                    [
                                        13,
                                        7.58
                                    ],
                                    [
                                        9,
                                        8.81
                                    ],
                                    [
                                        11,
                                        8.33
                                    ],
                                    [
                                        14,
                                        9.96
                                    ],
                                    [
                                        6,
                                        7.24
                                    ],
                                    [
                                        4,
                                        4.26
                                    ],
                                    [
                                        12,
                                        10.84
                                    ],
                                    [
                                        7,
                                        4.82
                                    ],
                                    [
                                        5,
                                        5.68
                                    ]
                                ]
                            },
                            {
                                "name": "scatter 2",
                                "data": [
                                    [
                                        10,
                                        8.04
                                    ],
                                    [
                                        8,
                                        6.95
                                    ],
                                    [
                                        13,
                                        7.58
                                    ],
                                    [
                                        9,
                                        5.81
                                    ],
                                    [
                                        4,
                                        4.26
                                    ],
                                    [
                                        12,
                                        10.84
                                    ],
                                    [
                                        7,
                                        4.82
                                    ],
                                    [
                                        5,
                                        5.68
                                    ]
                                ]
                            }
                        ]
                    },
                    "type": "SCATTER",
                    "fileId": 686,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/1/elements/61/files/686"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/1/elements/61/files/686/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/1/elements/61/files/686/boardThumbnail"
                        },
                        {
                            "rel": "preview",
                            "href": "/boards/1/elements/61/files/686/preview"
                        },
                        {
                            "rel": "downloadLink",
                            "href": "/boards/1/elements/61/files/686/downloadLink"
                        },
                        {
                            "rel": "temporaryPreviewLink",
                            "href": "/boards/1/elements/61/files/686/temporaryPreviewLink"
                        },
                        {
                            "rel": "comments",
                            "href": "/boards/1/elements/61/files/686/comments"
                        }
                    ]
                }
            }

## DELETE /boards/{boardId}/elements/{elementId}/files/{fileId}

+ Request 
    + Headers
    
            Accept: */*
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 ()

## PATCH /boards/{boardId}/elements/{elementId}/files/{fileId}

Possible types of charts are: `BAR`, `LINE`, `PIE`, `SCATTER`, and `RADAR`.

All the fields of a chart that include `axis`, and `title` can be updated.

For `BAR` and `LINE` charts it is not possible to update existing series and a add a new one simultaneously. 
If you want to do that, please make two separate request. 

When adding data to an existing `BAR` or `LINE` chart, 
requests body must contain all series in the existing chart, 
and size(series[i].data)==size(indicator.data).

It is possible to add a series in `BAR` and `LINE` charts. Added series should have a unique name,
different from all other names in the series, and should comply to size(series[i].data)==size(indicator.data).

For `LINE` charts `tooltip` is not a mandatory field for series data.
You can also exclude any of tooltips fields (`text`, `img`, `url`) from request. 

For `RADAR` chart size(data.indicator)==size(series[i].data.value), 
and charts series.data.value[i]<=data.indicator[i].max.


+ Request
    + Headers
    
            Accept: */*
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

    + Body
    
            {
                "file": {
                    "index": 1
                }
            }

+ Response 200 ()

+ Response 400 ()

        If index out of bounds


+ Request
    + Headers
    
            Content-Size: 345
            Content-Type: application/vnd.uberblik.htmlReference+json;charset=UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

    + Body
    
            {
                "htmlReference": {
                    "title" : "",
                    "titleThumb" : "", 
                }
            }

+ Response 200 ()


+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.chart+json
            access-token: uywg87gw6gf6g468gf46g4f6g34f4f4
            Content-Type: application/json;charset:UTF-8

    + Body
    
            {
                "chart":{
                    "title":"BarChart",
                    "type":"BAR",
                    "data":{
                        "series":[
                            {
                                "name":"NEW SERIES",
                                "data":[
                                    18203,
                                    23489,
                                    29034,
                                    104970,
                                    131744,
                                    630230
                                ]
                            }
                        ],
                        "xAxis":{
                            "data":[
                                "123",
                                "asd",
                                "1d2",
                                "d12",
                                "d3",
                                "d1"
                            ],
                            "name":"123"
                        },
                        "yAxis":{
                            "name":null
                        }
                    }
                }
            }

+ Response 201 (application/vnd.uberblik.chart+json; charset=utf-8)

    + Headers 

            x-uberblik-file-index: 23
            x-uberblik-filename: BarChart
    
    + Body
    
            {
                "chart": {
                    "title": "BarChart",
                    "data": {
                        "series": [
                            {
                                "name": "NEW SERIES",
                                "data": [
                                    18203,
                                    23489,
                                    29034,
                                    104970,
                                    131744,
                                    630230
                                ]
                            },
                            {
                                "name": "EXISTING",
                                "data": [
                                    182,
                                    289,
                                    234,
                                    10970,
                                    13144,
                                    60230
                                ]
                            }
                        ],
                        "xAxis": {
                            "data": [
                                "123",
                                "asd",
                                "1d2",
                                "d12",
                                "d3",
                                "d1"
                            ],
                            "name": "123"
                        },
                        "yAxis": {
                            "name": null
                        }
                    },
                    "type": "BAR",
                    "fileId": 681,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/1/elements/61/files/681"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/1/elements/61/files/681/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/1/elements/61/files/681/boardThumbnail"
                        },
                        {
                            "rel": "preview",
                            "href": "/boards/1/elements/61/files/681/preview"
                        },
                        {
                            "rel": "downloadLink",
                            "href": "/boards/1/elements/61/files/681/downloadLink"
                        },
                        {
                            "rel": "temporaryPreviewLink",
                            "href": "/boards/1/elements/61/files/681/temporaryPreviewLink"
                        },
                        {
                            "rel": "comments",
                            "href": "/boards/1/elements/61/files/681/comments"
                        }
                    ]
                }
            }

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.chart+json
            access-token: uywg87gw6gf6g468gf46g4f6g34f4f4
            Content-Type: application/json;charset:UTF-8

    + Body
    
            {
              "chart": {
                "title": "LineChart",
                "type": "LINE",
                "data": {
                  "series": [
                    {
                      "disabled": true,
                      "name": "NAME",
                      "data": [
                        {
                          "value": 820,
                          "tooltip": {
                            "text": "This is text. It is very interesting, and was written very beautifully.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                            "url": "https://alnedorezov.com"
                          }
                        },
                        {
                          "value": 244,
                          "tooltip": {
                            "text": "This is text 2. It is very interesting, and was written very beautifully.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                            "url": null
                          }
                        },
                        {
                          "value": 2432,
                          "tooltip": null
                        },
                        {
                          "value": 456,
                          "tooltip": null
                        },
                        {
                          "value": 896,
                          "tooltip": {
                            "text": null,
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        },
                        {
                          "value": 8532,
                          "tooltip": {
                            "text": "This is text 6. It is very interesting, and was written very beautifully.",
                            "img": null
                          }
                        }
                      ]
                    },
                    {
                      "name": "NAME1",
                      "data": [
                        {
                          "value": 4,
                          "tooltip": {
                            "text": "This is text. It is very interesting, and was written very beautifully.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        },
                        {
                          "value": 256
                        },
                        {
                          "value": 2466,
                          "tooltip": {
                            "text": "This is text 3. It is very interesting, and was written very beautifully.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        },
                        {
                          "value": 346,
                          "tooltip": {
                            "text": "This is text 4. It is very interesting, and was written very beautifully.",
                            "img": ""
                          }
                        },
                        {
                          "value": 8742,
                          "tooltip": {
                            "text": "Ururu. Kokoko.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        },
                        {
                          "value": 32432,
                          "tooltip": {
                            "text": "This is text 6. It is very interesting, and was written very beautifully.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        }
                      ]
                    },
                    {
                      "disabled": null,
                      "name": "NAME1",
                      "data": [
                        {
                          "value": 4,
                          "tooltip": {
                            "text": null,
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        },
                        {
                          "value": 256,
                          "tooltip": {
                            "text": "This is text 2. It is very interesting, and was written very beautifully.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        },
                        {
                          "value": 2466,
                          "tooltip": {
                            "text": "This is text 3. It is very interesting, and was written very beautifully.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        },
                        {
                          "value": 346,
                          "tooltip": {
                            "text": "This is text 4. It is very interesting, and was written very beautifully.",
                            "img": ""
                          }
                        },
                        {
                          "value": 8742,
                          "tooltip": {
                            "text": "",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg"
                          }
                        },
                        {
                          "value": 32432,
                          "tooltip": {
                            "text": "This is text 6. It is very interesting, and was written very beautifully.",
                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                            "url": ""
                          }
                        }
                      ]
                    }
                  ],
                  "xAxis": {
                    "data": [
                      "123",
                      "asd",
                      "1d2",
                      "d12",
                      "d3",
                      "d1"
                    ],
                    "name": "123"
                  },
                  "yAxis": {
                    "name": null
                  }
                }
              }
            }

+ Response 201 (application/vnd.uberblik.chart+json; charset=utf-8)

    + Headers 

            x-uberblik-file-index: 31
            x-uberblik-filename: LineChart
    
    + Body
    
            {
                "chart": {
                    "title": "LineChart",
                    "data": {
                        "series": [
                            {
                                "name": "NAME",
                                "data": [
                                    {
                                        "value": 820,
                                        "tooltip": {
                                            "text": "This is text. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": "https://alnedorezov.com"
                                        }
                                    },
                                    {
                                        "value": 244,
                                        "tooltip": {
                                            "text": "This is text 2. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 2432,
                                        "tooltip": null
                                    },
                                    {
                                        "value": 456,
                                        "tooltip": null
                                    },
                                    {
                                        "value": 896,
                                        "tooltip": {
                                            "text": null,
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 8532,
                                        "tooltip": {
                                            "text": "This is text 6. It is very interesting, and was written very beautifully.",
                                            "img": null,
                                            "url": null
                                        }
                                    }
                                ],
                                "disabled": true
                            },
                            {
                                "name": "NAME1",
                                "data": [
                                    {
                                        "value": 4,
                                        "tooltip": {
                                            "text": "This is text. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 256,
                                        "tooltip": null
                                    },
                                    {
                                        "value": 2466,
                                        "tooltip": {
                                            "text": "This is text 3. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 346,
                                        "tooltip": {
                                            "text": "This is text 4. It is very interesting, and was written very beautifully.",
                                            "img": "",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 8742,
                                        "tooltip": {
                                            "text": "Ururu. Kokoko.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 32432,
                                        "tooltip": {
                                            "text": "This is text 6. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    }
                                ],
                                "disabled": false
                            },
                            {
                                "name": "NAME1",
                                "data": [
                                    {
                                        "value": 4,
                                        "tooltip": {
                                            "text": null,
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 256,
                                        "tooltip": {
                                            "text": "This is text 2. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 2466,
                                        "tooltip": {
                                            "text": "This is text 3. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 346,
                                        "tooltip": {
                                            "text": "This is text 4. It is very interesting, and was written very beautifully.",
                                            "img": "",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 8742,
                                        "tooltip": {
                                            "text": "",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": null
                                        }
                                    },
                                    {
                                        "value": 32432,
                                        "tooltip": {
                                            "text": "This is text 6. It is very interesting, and was written very beautifully.",
                                            "img": "https://1.bp.blogspot.com/-hnS13LJFQXM/VtrvpW5gBZI/AAAAAAAABmc/CnnXPwl_INo/s1600/amc3.jpg",
                                            "url": ""
                                        }
                                    }
                                ],
                                "disabled": false
                            }
                        ],
                        "xAxis": {
                            "data": [
                                "123",
                                "asd",
                                "1d2",
                                "d12",
                                "d3",
                                "d1"
                            ],
                            "name": "123"
                        },
                        "yAxis": {
                            "name": null
                        }
                    },
                    "type": "LINE",
                    "fileId": 1261,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/1/elements/61/files/1261"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/1/elements/61/files/1261/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/1/elements/61/files/1261/boardThumbnail"
                        },
                        {
                            "rel": "preview",
                            "href": "/boards/1/elements/61/files/1261/preview"
                        },
                        {
                            "rel": "downloadLink",
                            "href": "/boards/1/elements/61/files/1261/downloadLink"
                        },
                        {
                            "rel": "temporaryPreviewLink",
                            "href": "/boards/1/elements/61/files/1261/temporaryPreviewLink"
                        },
                        {
                            "rel": "comments",
                            "href": "/boards/1/elements/61/files/1261/comments"
                        }
                    ]
                }
            }

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.chart+json;charset=UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            Content-Type: application/json;charset:UTF-8
                        
    + Body
    
            {
                "chart":{
                    "title":"PieChart",
                    "type":"PIE",
                    "data":{
                        "series":[
                            {
                                "name":"Name",
                                "data":[
                                    {
                                        "value":335,
                                        "name":"12345"
                                    },
                                    {
                                        "value":310,
                                        "name":"abvgdeika"
                                    },
                                    {
                                        "value":234,
                                        "name":"OLOLO"
                                    },
                                    {
                                        "value":135,
                                        "name":"Vulcanos"
                                    },
                                    {
                                        "value":1548,
                                        "name":"Carrots"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }

+ Response 201 (application/vnd.uberblik.chart+json; charset=utf-8)

    + Headers 

            x-uberblik-file-index: 24
            x-uberblik-filename: PieChart
            
    + Body
    
            {
                "chart":{
                    "title":"PieChart",
                    "data":{
                        "series":[
                            {
                                "name":"Name",
                                "data":[
                                    {
                                        "value":335,
                                        "name":"12345"
                                    },
                                    {
                                        "value":310,
                                        "name":"abvgdeika"
                                    },
                                    {
                                        "value":234,
                                        "name":"OLOLO"
                                    },
                                    {
                                        "value":135,
                                        "name":"Vulcanos"
                                    },
                                    {
                                        "value":1548,
                                        "name":"Carrots"
                                    }
                                ]
                            }
                        ]
                    },
                    "type":"PIE",
                    "fileId":483,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/243/elements/472/files/483"
                        },
                        {
                            "rel":"thumbnail",
                            "href":"/boards/243/elements/472/files/483/thumbnail"
                        },
                        {
                            "rel":"boardThumbnail",
                            "href":"/boards/243/elements/472/files/483/boardThumbnail"
                        },
                        {
                            "rel":"preview",
                            "href":"/boards/243/elements/472/files/483/preview"
                        },
                        {
                            "rel":"downloadLink",
                            "href":"/boards/243/elements/472/files/483/downloadLink"
                        },
                        {
                            "rel":"temporaryPreviewLink",
                            "href":"/boards/243/elements/472/files/483/temporaryPreviewLink"
                        },
                        {
                            "rel":"comments",
                            "href":"/boards/243/elements/472/files/483/comments"
                        }
                    ]
                }
            }

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.chart+json;charset=UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            Content-Type: application/json;charset:UTF-8
                        
    + Body
    
            {
                "chart":{
                    "title":"RadarChart",
                    "type":"RADAR",
                    "data":{
                        "indicator":[
                            {
                                "name":"销售（sales）",
                                "max":6500
                            },
                            {
                                "name":"管理（Administration）",
                                "max":16000
                            },
                            {
                                "name":"信息技术（Information Techology）",
                                "max":30000
                            },
                            {
                                "name":"客服（Customer Support）",
                                "max":38000
                            },
                            {
                                "name":"研发（Development）",
                                "max":52000
                            },
                            {
                                "name":"市场（Marketing）",
                                "max":25000
                            }
                        ],
                        "series":[
                            {
                                "name":"预算 vs 开销（Budget vs spending）",
                                "data":[
                                    {
                                        "value":[
                                            4300,
                                            10000,
                                            28000,
                                            35000,
                                            50000,
                                            19000
                                        ],
                                        "name":"预算分配（Allocated Budget）"
                                    },
                                    {
                                        "value":[
                                            5000,
                                            14000,
                                            28000,
                                            31000,
                                            42000,
                                            21000
                                        ],
                                        "name":"实际开销（Actual Spending）"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }

+ Response 201 (application/vnd.uberblik.chart+json; charset=utf-8)

    + Headers 

            x-uberblik-file-index: 25
            x-uberblik-filename: RadarChart
            
    + Body
    
            {
                "chart":{
                    "title":"RadarChart",
                    "data":{
                        "indicator":[
                            {
                                "name":"销售（sales）",
                                "max":6500
                            },
                            {
                                "name":"管理（Administration）",
                                "max":16000
                            },
                            {
                                "name":"信息技术（Information Techology）",
                                "max":30000
                            },
                            {
                                "name":"客服（Customer Support）",
                                "max":38000
                            },
                            {
                                "name":"研发（Development）",
                                "max":52000
                            },
                            {
                                "name":"市场（Marketing）",
                                "max":25000
                            }
                        ],
                        "series":[
                            {
                                "name":"预算 vs 开销（Budget vs spending）",
                                "data":[
                                    {
                                        "value":[
                                            4300,
                                            10000,
                                            28000,
                                            35000,
                                            50000,
                                            19000
                                        ],
                                        "name":"预算分配（Allocated Budget）"
                                    },
                                    {
                                        "value":[
                                            5000,
                                            14000,
                                            28000,
                                            31000,
                                            42000,
                                            21000
                                        ],
                                        "name":"实际开销（Actual Spending）"
                                    }
                                ]
                            }
                        ]
                    },
                    "type":"RADAR",
                    "fileId":523,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/1/elements/1/files/523"
                        },
                        {
                            "rel":"thumbnail",
                            "href":"/boards/1/elements/1/files/523/thumbnail"
                        },
                        {
                            "rel":"boardThumbnail",
                            "href":"/boards/1/elements/1/files/523/boardThumbnail"
                        },
                        {
                            "rel":"preview",
                            "href":"/boards/1/elements/1/files/523/preview"
                        },
                        {
                            "rel":"downloadLink",
                            "href":"/boards/1/elements/1/files/523/downloadLink"
                        },
                        {
                            "rel":"temporaryPreviewLink",
                            "href":"/boards/1/elements/1/files/523/temporaryPreviewLink"
                        },
                        {
                            "rel":"comments",
                            "href":"/boards/1/elements/1/files/523/comments"
                        }
                    ]
                }
            }

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.chart+json;charset=UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            Content-Type: application/json;charset:UTF-8
                        
    + Body
    
            {
                "chart":{
                    "title":"ScatterChart",
                    "type":"SCATTER",
                    "data":{
                        "xAxis":{
                            "name":"123"
                        },
                        "yAxis":{
                            "name":null
                        },
                        "series":[
                            {
                                "name":"scatter 1",
                                "data":[
                                    [
                                        10.0,
                                        8.04
                                    ],
                                    [
                                        8.0,
                                        6.95
                                    ],
                                    [
                                        13.0,
                                        7.58
                                    ],
                                    [
                                        9.0,
                                        8.81
                                    ],
                                    [
                                        11.0,
                                        8.33
                                    ],
                                    [
                                        14.0,
                                        9.96
                                    ],
                                    [
                                        6.0,
                                        7.24
                                    ],
                                    [
                                        4.0,
                                        4.26
                                    ],
                                    [
                                        12.0,
                                        10.84
                                    ],
                                    [
                                        7.0,
                                        4.82
                                    ],
                                    [
                                        5.0,
                                        5.68
                                    ]
                                ]
                            },
                            {
                                "name":"scatter 2",
                                "data":[
                                    [
                                        10.0,
                                        8.04
                                    ],
                                    [
                                        8.0,
                                        6.95
                                    ],
                                    [
                                        13.0,
                                        7.58
                                    ],
                                    [
                                        9.0,
                                        5.81
                                    ],
                                    [
                                        4.0,
                                        4.26
                                    ],
                                    [
                                        12.0,
                                        10.84
                                    ],
                                    [
                                        7.0,
                                        4.82
                                    ],
                                    [
                                        5.0,
                                        5.68
                                    ]
                                ]
                            }
                        ]
                    }
                }
            }
    
+ Response 201 (application/vnd.uberblik.chart+json; charset=utf-8)

    + Headers 

            x-uberblik-file-index: 26
            x-uberblik-filename: ScatterChart
            
    + Body
    
            {
                "chart": {
                    "title": "ScatterChart",
                    "data": {
                        "xAxis": {
                            "name": "123"
                        },
                        "yAxis": {
                            "name": null
                        },
                        "series": [
                            {
                                "name": "scatter 1",
                                "data": [
                                    [
                                        10,
                                        8.04
                                    ],
                                    [
                                        8,
                                        6.95
                                    ],
                                    [
                                        13,
                                        7.58
                                    ],
                                    [
                                        9,
                                        8.81
                                    ],
                                    [
                                        11,
                                        8.33
                                    ],
                                    [
                                        14,
                                        9.96
                                    ],
                                    [
                                        6,
                                        7.24
                                    ],
                                    [
                                        4,
                                        4.26
                                    ],
                                    [
                                        12,
                                        10.84
                                    ],
                                    [
                                        7,
                                        4.82
                                    ],
                                    [
                                        5,
                                        5.68
                                    ]
                                ]
                            },
                            {
                                "name": "scatter 2",
                                "data": [
                                    [
                                        10,
                                        8.04
                                    ],
                                    [
                                        8,
                                        6.95
                                    ],
                                    [
                                        13,
                                        7.58
                                    ],
                                    [
                                        9,
                                        5.81
                                    ],
                                    [
                                        4,
                                        4.26
                                    ],
                                    [
                                        12,
                                        10.84
                                    ],
                                    [
                                        7,
                                        4.82
                                    ],
                                    [
                                        5,
                                        5.68
                                    ]
                                ]
                            }
                        ]
                    },
                    "type": "SCATTER",
                    "fileId": 686,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/1/elements/61/files/686"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/1/elements/61/files/686/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/1/elements/61/files/686/boardThumbnail"
                        },
                        {
                            "rel": "preview",
                            "href": "/boards/1/elements/61/files/686/preview"
                        },
                        {
                            "rel": "downloadLink",
                            "href": "/boards/1/elements/61/files/686/downloadLink"
                        },
                        {
                            "rel": "temporaryPreviewLink",
                            "href": "/boards/1/elements/61/files/686/temporaryPreviewLink"
                        },
                        {
                            "rel": "comments",
                            "href": "/boards/1/elements/61/files/686/comments"
                        }
                    ]
                }
            }

## GET /boards/{id}/elements/{elementId}/files/{fileId}/comments

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.fileCommentList+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200
    
    + Body
    
            {
                "fileCommentList": [
                    {
                        "message":"Post message",
                        "created":1395070480487,
                        "_links":
                        [
                            {"rel":"self","href":"/boards/6637/elements/7862345/files/234/comments/424"},
                            {"rel":"author","href":"/users/1"}
                        ]
                    },
                    {
                        "message":"this file is very interesting blah blah",
                        "created":1395070480497,
                        "_links":
                        [
                            {"rel":"self","href":"/boards/6637/elements/7862345/files/234/comments/425"},
                            {"rel":"author","href":"/users/1"}
                        ]
                    }
                ]
            }

## POST /boards/{id}/elements/{elementId}/files/{fileId}/comments

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.fileComment+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4


    + Body
    
            {
                "fileComment":
                {
                    "message":"This is a post or comment to a file"
                }
            }


+ Response 201

    + Body
    
            {
                "fileComment":{
                    "message":"This is a post or comment to a file",
                    "created":1514210974582,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/boards/1/elements/1/files/1/comments/1101"
                        },
                        {
                            "rel":"author",
                            "href":"/users/1"
                        }
                    ]
                }
            }

## GET /boards/{id}/elements/{elementId}/files/{fileId}/comments/{fileCommentId}

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.fileComment+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200

    + Body
    
            {
                "fileComment":
                {
                    "message":"This is a post or comment to a file",
                    "created": 123384747473
                    "_links" :
                    [
                        {"rel":"self","href":"/boards/6637/elements/7862345/files/234/comments/425"},
                        {"rel":"author","href":"/users/1"}
                    ]
                }
            }

## DELETE /boards/{id}/elements/{elementId}/files/{fileId}/comments/{fileCommentId}

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.fileComment+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200


## GET /boards/{id}/elements/{elementId}/files/{fileId}/thumbnail

+ Request
    + Headers
    
            Accept: image/jpg, image/png, image/gif, application/pdf

+ Response 200 
    + Headers 

            Content-Length: 346245
            Content-Type: image/jpeg
            
    + Body
    
            gh6f6g346gf3g46r346rr4h9d273hd293hh32...

## GET /boards/{boardId}/elements/{elementId}/files/{fileId}/boardThumbnail

+ Request
    + Headers
    
            Accept: image/jpg, image/png, image/gif, application/pdf

+ Response 200 
    + Headers 

            Content-Length: 346245
            Content-Type: image/jpeg
            
    + Body
    
            gh6f6g346gf3g46r346rr4h9d273hd293hh32...

## GET /boards/{boardId}/elements/{elementId}/files/{fileId}/activityThumbnail

Will return 404 NOT_FOUND for charts and html references, 
as they do not require activity thumbnails according to the design mockups.

+ Request
    + Headers
    
            Accept: image/jpg, image/png, image/gif, application/pdf

+ Response 200 
    + Headers 

            Content-Length: 346245
            Content-Type: image/jpeg
            
    + Body
    
            gh6f6g346gf3g46r346rr4h9d273hd293hh32...

## HEAD /boards/{boardId}/elements/{elementId}/files/{fileId}/preview{?viewportHeight}

+ Response 200 ()
    + Headers 

            Content-Length : 346245
            x-uberblik-image-height : 200
            x-uberblik-image-width : 200
            x-uberblik-viewport-height : 180
            x-uberblik-viewport-width : 180


## POST /boards/{boardId}/elements/{elementId}/files/{fileId}/temporaryPreviewLink{?viewportHeight}
+ Request
    + Headers
    
            Accept: image/jpg

+ Response 400 ()

    + Headers 
    
            x-uberblik-error : HeightRequired ... the height parameter was omitted.

+ Response 201 
    + Headers
    
            Content-Type: application/vnd.uberblik.temporaryPreviewLink+json;charset=UTF-8


    + Body
    
            {
                "temporaryPreviewLink" : {
                    "url" : "/preview/businessPlan.pdf?token=6t2r63t4rt673g6737fghq7hcbghfhjsg6g4ux2sw28
                }
            }
            
## GET /boards/{boardId}/elements/{elementId}/files/{fileId}/preview{?viewportHeight}
+ Request
    + Headers
    
            Accept: image/jpg

+ Response 400 ()

    + Headers 
    
            x-uberblik-error : HeightRequired ... the height parameter was omitted.


+ Response 200 
    + Headers 

            Content-Length: 346245
            Content-Type: image/jpeg
            
    + Body
    
            gh6f6g346gf3g46r346rr4h9d273hd293hh32...
            
# Group Access tokens

The `POST /accesstokens` resource is the only resource that is secured via basic auth and the only
resource (besides root `/` and ping `/ping`) than can be called without providing an `access-token` header.<br>

In other words, a user has to authenticate against the server only when creating a new access token. After
that, the client has to store the token and use it in each subsequent request. Should a token 
become invalid or simply expire, the next request with that token would result in a `HTTP 403 (Forbidden)` response. 
Upon such a response, the client has to enable the user to create a new token.

### Deleting a token

In the REST world there is no notion of "logged in" or "logged out". Also there are no sessions,
as this would break the REST principle of statelessness. Still a user can delete the current token
to force the client to create a new one, thus requesting the user's credentials again. When a client 
deletes a token, the token gets invalidated and any open web socket to that client is closed.

Common http codes returned by operations on tokens:

+ `200` when sucessfully retrieved or deleted a token
+ `201` when a new token was successfully created
+ `401` when the basic auth fails


## POST /accesstokens

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.accessTokenRequest+json;charset:UTF-8
            Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==

    + Body 
    
            {
                "accessTokenRequest" : 
                {
                    "clientId": "we2$%6etetertef",
                    "grantType": "password"
                }
            }

+ Response 201 ( application/vnd.uberblik.accessToken+json) 

    + Body
    
            {
                "accessToken": 
                {
                    "token": "$54eritet%&3",
                    "secret": "er34%rt34%f",
                    "clientId": "we2$%6etetertef",
                     "_links" : [
                        { "rel": "self", "href": "/accesstokens" },
                        { "rel" : "user", "href" : "/users/1" }
                    ]   
                }
            } 

+ Response 401 
    + Headers
    
            WWW-Authenticate: Basic realm="Uberblik-Api"


## DELETE /accesstokens

+ Response 200


# Group Activities

Activities represent summaries of actions performed on the system. They are available either for a single board (`/boards/{boardId}/activities`) or for all boards that the current user has access to (`/activities`).
In the future, other targets might be added.<br>

Activities can relate to several different aspects of the system's usage. Therefore, each activity has specific fields (inside `details`) that are not equal across all activities. We've tried to unify the structure of an activity as much as possible. The followings notes should make parsing activities easier: 

+ Every activity is of content type `application/vnd.uberblik.activity+json`
+ Every activity has a `published` field in their JSON's root, which is 
the timestamp of the time when the activity was recorded.
+ Every activity has a unique `type`. The available types are listed below.
+ Every activity has a `details`field that provide semantic details of the acitivity that are specific for the activity type.
+ `_links` are in so far different from other _links that they are specific to the activity type and available references can change over time. See the `Possible actions` column below.
+ Every activity has a `state` that can be `VALID` (possible activity states are: `VALID`, `MERGED`, `RESTORED`, `DELETED`, and `INVALID`).
+ Every activity has a `displayText` field that describes the activity

The following table describes the available activitie types:

| Type          | Description           |Possible actions| Possible states | Notes |
| :---------------------|:----------------------------------|:-------------| :-----------------|:-----------------| 
| UserLoggedIn  |A user created a new access token  |n/a|VALID, USER_DELETED(TODO)        ||
| UserLoggedOut   |A user deleted an access token   |n/a|VALID, USER_DELETED(TODO)         |         
| PostedToBoard       |A user posted something to a board |erase(TODO: not implemented yet),restore|VALID, AUTHOR_DELETED(TODO)         |
| PostRestored      | A user restored a post      |restore| VALID, AUTHOR_DELETED(TODO)||
| ElementEditedCaption     | A user edited the caption of an element|n/a   | VALID, MERGED||
| ElementRemoved    | A user removed the element      |erase,restore|VALID, MERGED, RESTORED||
| ElementAdded      | A user added an element       |n/a|VALID, MERGED||
| ElementRestored   | A user restored an element      |n/a|VALID, MERGED||
| FileRemoved     | A user removed a file         |erase,restore|VALID, MERGED, RESTORED||
| FileRestored      | A user restored a file        |n/a|VALID, MERGED||
| FiledAdded      | A user added a file         |n/a|VALID, MERGED||
| HtmlRefRemoved     | A user removed an htmlref type file         |erase,restore|VALID, MERGED, RESTORED||
| HtmlRefRestored      | A user restored an htmlref type file        |n/a|VALID, MERGED||
| HtmlRefAdded      | A user added an htmlref type file         |n/a|VALID, MERGED||
| ElementMerged     | A user merged two elements or from archive|n/a|VALID, MERGED||
| FileCommented     | A user added a comment to a file    |erase(TODO: not implemented yet)|VALID, MERGED||
| HtmlRefCommented     | A user added a comment to an htmlref type file    |erase|VALID, AUTHOR_DELETED(TODO),MERGED||
| UserCreatedBoard     | A user created this board    |n/a|VALID, USER_DELETED(TODO)| This is the first activity on a board.|
| UserInvited     | A user was invited to the board    |n/a|VALID, USER_DELETED(TODO)||
| UserJoinedBoard    | A user joined the board    |n/a|VALID, USER_DELETED(TODO)||
| UserLeftBoard     | A user left the board    |n/a|VALID, USER_DELETED(TODO)||



Common http codes returned by operations on activities:

+ `200` when sucessfully retrieved or deleted an activity
+ `403` returned if the token is expired, invalid or not found

### Optional date range filter

A subset of activities can be retrieved by provding a date range of the published timestamp:

* `from`: return activities that were published after this date (inclusive)
* `to`: return activities that were published before this date (inclusive)
* `limit`: maximum number of activities to be returned. Activities are orders published desc (newest first) 

`from` and `to` are optional, both, one or none can be provided 


### Restoring an activity

Some activities can be used to create objects on the board. By placing an activity on the board 
an element gets created according to the activity. For example, restoring a "user removed the element" activity
will re-create that element on the new position. See the table below for a complete list.

If an activity can not be used to create an element, an error code `400: ActivityNotRestorable` will be returned.

Response http codes:

+ `201` when sucessfully restored an activity
+ `400` when the activity not restorable
+ `409` when there is a conflict, e.g. position already occupied


| Activity                | Result of restoration      |
| :-------------------------------------|:-------------------------------| 
| A user posted something to a board  |New element with post as caption| 
| A user removed the element      |The removed element restored with files and caption. Action removed.| 
| A user removed a file         |The removed file restored with a new element. Action removed.|
| A user removed an htmlref type file |The removed htmlref file restored with a new element. Action removed.|
| A user created a new access token   |Not restorable 400| 
| A user deleted an access token    |Not restorable 400| 
| A user edited the caption of an element|Not restorable 400| 
| A user added an element       |Not restorable 400| 
| A user added a file         |Not restorable 400| 


Below are examples for each of the activity types mentioned in the table above:

## UserLoggedIn

```
{
  "activity": { 
    "type": "UserLoggedIn",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian logged in",
    "details": {
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"}
    ]
   }
}
```

## UserLoggedOut

```
{
  "activity": { 
    "type": "UserLoggedOut",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian logged out",
    "details": {
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"}
    ]
   }
}
```

## PostedToBoard

```
{
  "activity": { 
    "type": "PostedToBoard",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian posted 'hi' to the board",
    "details": {
        "boardName" : "myBoard",
      "post": "a new post"
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "restore", "href": "/activities/3/restore"},
        {"rel": "erase", "href": "/boards/1/posts/12"},
        {"rel": "board", "href": "/boards/1"}
    ]
   }
}
```

## PostRestored

```
{
  "activity": { 
    "type": "PostRestored",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian restored the post 'hi'",
    "details": {
    "boardName" : "myBoard",
      "post": "a new post"
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "restore", "href": "/activities/3/restore"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "board", "href":  "/boards/81"}
    ]
   }
}
```

## ElementEditedCaption

```
{
  "activity": { 
    "type": "ElementEditedCaption",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian edited the element 1,1",
    "details": {
      "boardName" : "myBoard",
      "newCaption": "a new caption"
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "board", "href":  "/boards/81"},
        {"rel": "element", "href":  "/boards/81/elements/3"}
        {"rel": "elementThumbnail", "href": "/boards/81/elements/222/thumbnail"},
    ]
   }
}
```


## ElementRemoved

```
{
  "activity": { 
    "type": "ElementRemoved",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian removed the element 1,1",
    "details": {
      "boardName" : "myBoard",
      "elementCaption": "my files"
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "restore", "href": "/activities/3/restore"},
        {"rel": "erase", "href": "/boards/81/elements/222"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "element", "href": "/boards/81/elements/222"},
        {"rel": "elementThumbnail", "href": "/boards/81/elements/222/thumbnail"},
        {"rel": "board", "href":  "/boards/81"}
    ]
   }
}
```

## ElementAdded

```
{
  "activity": { 
    "type": "ElementAdded",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian added the element 1,1",
    "details": {
      "boardName" : "myBoard",
      "elementCaption": "",
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "element", "href": "/boards/81/elements/222"},
        {"rel": "elementThumbnail", "href": "/boards/81/elements/222/thumbnail"},
        {"rel": "board", "href":  "/boards/81"}
    ]
   }
}
```

## ElementRestored

```
{
  "activity": { 
    "type": "ElementRestored",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian restored the element 1,1",
    "details": {
      "boardName" : "myBoard",
      "elementCaption": "a caption"
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "element", "href": "/boards/81/elements/222"},
        {"rel": "elementThumbnail", "href": "/boards/81/elements/222/thumbnail"},
        {"rel": "board", "href":  "/boards/81"}
    ]
   }
}
```

## ElementMerged

```
{
  "activity": { 
    "type": "ElementMerged",
    "published": 1397023355854,
    "displayText": "Sebastian merged the element 1,1",
    "state": "VALID",
    "details": {
      "boardName" : "myBoard",
      "elementCaption": "more files"
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "element", "href": "/boards/81/elements/222"},
        {"rel": "elementThumbnail", "href": "/boards/81/elements/222/thumbnail"},
        {"rel": "board", "href":  "/boards/81"}
    ]
   }
}
```

## FileRemoved  

```
{
  "activity": { 
    "type": "FileRemoved",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian removed the file report.pdf",
    "details": {
      "boardName" : "myBoard",
      "fileName": "report.pdf",
      "fileType": "application/pdf"
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "restore", "href": "/activities/3/restore"},
        {"rel": "erase", "href": "/boards/81/elements/225/files/283"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "file", "href": "/boards/81/elements/222/files/284"},
        {"rel": "fileThumbnail", "href": "/boards/81/elements/222/files/284/thumbnail"},
        {"rel": "element", "href": "/boards/81/elements/222"},
        {"rel": "board", "href":  "/boards/81"}
    ]
   }
}
```

## FileRestored

```
{
    "activity": { 
        "type": "FileRestored",
        "published": 1397023355854,
        "state": "VALID",
        "displayText": "Sebastian restored the file report.pdf",
        "details": {
            "boardName" : "myBoard",
            "fileName": "report.pdf",
            "fileType": "application/pdf"
        },
        "author":{
            "id":1,
            "firstName":"Aleksandr",
            "lastName":"Nedorezov",
            "email": "nedorezov@own.space"
        },
        "_links": [
            {"rel": "self", "href": "/activities/3"},
            {"rel": "author", "href": "/users/1"},
            {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
            {"rel": "file", "href": "/boards/81/elements/222/files/284"},
            {"rel": "fileThumbnail", "href": "/boards/81/elements/222/files/284/thumbnail"},
            {"rel": "element", "href": "/boards/81/elements/222"},
            {"rel": "board", "href":  "/boards/81"}
        ]
    }
}
```

## FiledAdded

```
{
  "activity": { 
    "type": "FileAdded",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian added the file report.pdf",
    "details": {
      "boardName" : "myBoard",
      "fileName": "report.pdf",
      "fileType": "application/pdf"
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "file", "href": "/boards/81/elements/222/files/284"},
        {"rel": "fileThumbnail", "href": "/boards/81/elements/222/files/284/thumbnail"},
        {"rel": "element", "href": "/boards/81/elements/222"},
        {"rel": "board", "href":  "/boards/81"}
    ]
   }
}
```

## FileCommented

```
{
  "activity": { 
    "type": "FileCommented",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian commented the file report.pdf",
    "details": {
      "boardName" : "myBoard",
      "comment": "Nice url",
      "fileType": "application/vnd.uberblik.htmlReference",
      "fileName": "http://www.spiegel.de/some-new-article"
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "erase", "href": "/boards/81/elements/225/files/283"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "file", "href": "/boards/81/elements/222/files/284"},
        {"rel": "fileThumbnail", "href": "/boards/81/elements/222/files/284/thumbnail"},
        {"rel": "element", "href": "/boards/81/elements/222"},
        {"rel": "board", "href":  "/boards/81"}
    ]
   }
}
```

## HtmlRefRemoved  

```
{
  "activity": { 
    "type": "HtmlRefRemoved",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian removed the url http://www.spiegel.de",
    "details": {
      "boardName" : "myBoard",
      "urlTitle": "Spiegel Online",
      "url" : "http://www.spiegel.de",
      "fileType": "application/vnd.uberblik.htmlReference",
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "restore", "href": "/activities/3/restore"},
        {"rel": "erase", "href": "/boards/81/elements/225/files/283"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "file", "href": "/boards/81/elements/222/files/284"},
        {"rel": "fileThumbnail", "href": "/boards/81/elements/222/files/284/thumbnail"},
        {"rel": "element", "href": "/boards/81/elements/222"},
        {"rel": "board", "href":  "/boards/81"}
    ]
   }
}
```

## HtmlRefRestored

```
{
    "activity": { 
        "type": "HtmlRefRestored",
        "published": 1397023355854,
        "state": "VALID",
        "displayText": "Sebastian restored the url http://www.spiegel.de",
        "details": {
            "boardName" : "myBoard",
            "urlTitle": "Spiegel Online",
            "url" : "http://www.spiegel.de",
            "fileType": "application/vnd.uberblik.htmlReference",
        },
        "author":{
            "id":1,
            "firstName":"Aleksandr",
            "lastName":"Nedorezov",
            "email": "nedorezov@own.space"
        },
        "_links": [
            {"rel": "self", "href": "/activities/3"},
            {"rel": "author", "href": "/users/1"},
            {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
            {"rel": "file", "href": "/boards/81/elements/222/files/284"},
            {"rel": "fileThumbnail", "href": "/boards/81/elements/222/files/284/thumbnail"},
            {"rel": "element", "href": "/boards/81/elements/222"},
            {"rel": "board", "href":  "/boards/81"}
        ]
    }
}
```

## HtmlRefAdded

```
{
  "activity": { 
    "type": "HtmlRefAdded",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian added the url http://www.spiegel.de",
    "details": {
      "boardName" : "myBoard",
      "urlTitle": "Spiegel Online",
      "url" : "http://www.spiegel.de",
      "fileType": "application/vnd.uberblik.htmlReference",
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "file", "href": "/boards/81/elements/222/files/284"},
        {"rel": "fileThumbnail", "href": "/boards/81/elements/222/files/284/thumbnail"},
        {"rel": "element", "href": "/boards/81/elements/222"},
        {"rel": "board", "href":  "/boards/81"}
    ]
   }
}
```

## HtmlRefCommented

```
{
  "activity": { 
    "type": "HtmlRefCommented",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian commented the file report.pdf",
    "details": {
      "boardName" : "myBoard",
      "comment": "Nice url",
      "fileType": "application/vnd.uberblik.htmlReference",
      "urlTitle": "Spiegel Online",
      "url" : "http://www.spiegel.de",
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "erase", "href": "/boards/81/elements/225/files/283"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "file", "href": "/boards/81/elements/222/files/284"},
        {"rel": "fileThumbnail", "href": "/boards/81/elements/222/files/284/thumbnail"},
        {"rel": "element", "href": "/boards/81/elements/222"},
        {"rel": "board", "href":  "/boards/81"}
    ]
   }
}

```

## UserCreatedBoard

```
{
  "activity": { 
    "type": "UserCreatedBoard",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian created the board myBoard",
    "details": {
        "boardName" : "myBoard"
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "board", "href":  "/boards/81"}
    ]
   }
}
```
## UserInvited

Note that fields `invitee` and `inviteeThumbnail` will not be returned if invitation was deleted, e.g. if invited user was removed from the board.
In such a case empty image should be displayed instead of users avatar.

```
{
  "activity": { 
    "type": "UserInvited",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian was invited to board myBoard",
    "details": {
        "boardName" : "myBoard",
        "inviteeName" : "Sebastian"
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "invitee", "href": "/users/120"},
        {"rel": "inviteeThumbnail", "href": "/users/120/profileThumbnail"},
        {"rel": "board", "href":  "/boards/81"}
    ]
   }
}
```

## UserJoinedBoard

```
{
  "activity": { 
    "type": "UserJoinedBoard",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian joined the board myBoard",
    "details": {
        "boardName" : "myBoard"
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "board", "href":  "/boards/81"}
    ]
   }
}
```

## UserLeftBoard

```
{
  "activity": { 
    "type": "UserLeftBoard",
    "published": 1397023355854,
    "state": "VALID",
    "displayText": "Sebastian left the board myBoard",
    "details": {
        "boardName" : "myBoard"
    },
    "author":{
        "id":1,
        "firstName":"Aleksandr",
        "lastName":"Nedorezov",
        "email": "nedorezov@own.space"
    },
    "_links": [
        {"rel": "self", "href": "/activities/3"},
        {"rel": "author", "href": "/users/1"},
        {"rel": "authorThumbnail", "href": "/users/1/profileThumbnail"},
        {"rel": "board", "href":  "/boards/81"}
    ]
   }
}
```

## GET /activities?from={from}&to={to}&limit={limit}&state={state}

If a `limit` count is given, no more than that many activity will be returned (but possibly less,
if the query itself yields less rows). Negative or equal 0 limit is the same as omitting the `limit` clause.

Parameters `from` and `to` represent the time bounds in milliseconds 
(between the wanted time and midnight, January 1, 1970 UTC).
If they are set, only activities made from time passed in `from` and to time passed in `to` will be returned.

If `state` parameter is set, only activities of with this state are returned, 
otherwise request returns activities with all possible states.
States can be `VALID`, `MERGED`, `RESTORED`, `DELETED`, and `INVALID`.

Usage of parameters `from`, `to`, `limit`, and `state` is not mandatory.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.activities+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4


+ Response 200 (application/vnd.uberblik.activities+json)

    + Body
    
            {
                "activities":[
                    {
                        "type":"ElementRestored",
                        "published":1522347021470,
                        "displayText":"[Thu Mar 29 21:10:21 MSK 2018] Aleksandr restored element <6,2> to Welcome to OWN",
                        "details":{
                            "elementCaption":"this is a test element"
                        },
                        "state":"VALID",
                        "author":{
                            "id":1,
                            "firstName":"Aleksandr",
                            "lastName":"Nedorezov",
                            "email": "nedorezov@own.space"
                        },
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/activities/401"
                            },
                            {
                                "rel":"author",
                                "href":"/users/1"
                            },
                            {
                                "rel":"authorThumbnail",
                                "href":"/users/1/profileThumbnail"
                            },
                            {
                                "rel":"board",
                                "href":"/boards/1"
                            },
                            {
                                "rel":"element",
                                "href":"/boards/1/elements/1"
                            },
                            {
                                "rel":"elementThumbnail",
                                "href":"/boards/1/elements/1/thumbnail"
                            }
                        ]
                    },
                    {
                        "type":"HtmlRefAdded",
                        "published":1522324447014,
                        "displayText":"[Thu Mar 29 14:54:07 MSK 2018] Aleksandr added url <https://yandex.ru> to element <3,2> to Welcome to OWN",
                        "details":{
                            "urlTitle":"Яндекс",
                            "url":"https://yandex.ru",
                            "fileType":"application/vnd.uberblik.htmlReference"
                        },
                        "state":"VALID",
                        "author":{
                            "id":1,
                            "firstName":"Aleksandr",
                            "lastName":"Nedorezov",
                            "email": "nedorezov@own.space"
                        },
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/activities/321"
                            },
                            {
                                "rel":"author",
                                "href":"/users/1"
                            },
                            {
                                "rel":"authorThumbnail",
                                "href":"/users/1/profileThumbnail"
                            },
                            {
                                "rel":"file",
                                "href":"/boards/1/elements/1/files/21"
                            },
                            {
                                "rel":"fileThumbnail",
                                "href":"/boards/1/elements/1/files/21/thumbnail"
                            },
                            {
                                "rel":"element",
                                "href":"/boards/1/elements/1"
                            },
                            {
                                "rel":"board",
                                "href":"/boards/1"
                            }
                        ]
                    },
                    {
                        "type":"FileCommented",
                        "published":1522061733704,
                        "displayText":"[Mon Mar 26 13:55:33 MSK 2018] Aleksandr commented a file awddaw to Welcome to OWN",
                        "details":{
                            "fileName":"камазазаза",
                            "fileType":"image/jpeg",
                            "comment":"awddaw"
                        },
                        "state":"VALID",
                        "author":{
                            "id":1,
                            "firstName":"Aleksandr",
                            "lastName":"Nedorezov",
                            "email": "nedorezov@own.space"
                        },
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/activities/223"
                            },
                            {
                                "rel":"author",
                                "href":"/users/1"
                            },
                            {
                                "rel":"authorThumbnail",
                                "href":"/users/1/profileThumbnail"
                            },
                            {
                                "rel":"file",
                                "href":"/boards/1/elements/1/files/1"
                            },
                            {
                                "rel":"fileThumbnail",
                                "href":"/boards/1/elements/1/files/1/thumbnail"
                            },
                            {
                                "rel":"element",
                                "href":"/boards/1/elements/1"
                            },
                            {
                                "rel":"board",
                                "href":"/boards/1"
                            },
                            {
                                "rel":"restore",
                                "href":"/activities/223/restore"
                            },
                            {
                                "rel":"erase",
                                "href":"/boards/1/elements/1/files/1/comments/223"
                            }
                        ]
                    },
                    {
                        "type":"FileAdded",
                        "published":1522061726516,
                        "displayText":"[Mon Mar 26 13:55:26 MSK 2018] Aleksandr added file <камазазаза> to element <3,2> to Welcome to OWN",
                        "details":{
                            "fileName":"камазазаза",
                            "fileType":"image/jpeg"
                        },
                        "state":"VALID",
                        "author":{
                            "id":1,
                            "firstName":"Aleksandr",
                            "lastName":"Nedorezov",
                            "email": "nedorezov@own.space"
                        },
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/activities/222"
                            },
                            {
                                "rel":"author",
                                "href":"/users/1"
                            },
                            {
                                "rel":"authorThumbnail",
                                "href":"/users/1/profileThumbnail"
                            },
                            {
                                "rel":"file",
                                "href":"/boards/1/elements/1/files/1"
                            },
                            {
                                "rel":"fileThumbnail",
                                "href":"/boards/1/elements/1/files/1/thumbnail"
                            },
                            {
                                "rel":"element",
                                "href":"/boards/1/elements/1"
                            },
                            {
                                "rel":"board",
                                "href":"/boards/1"
                            }
                        ]
                    },
                    {
                        "type":"UserJoinedBoard",
                        "published":1520860463514,
                        "displayText":"[Mon Mar 12 16:14:23 MSK 2018] Aleksandr joined the board Welcome to OWN",
                        "details":{
                            "boardName":"Welcome to OWN"
                        },
                        "state":"VALID",
                        "author":{
                            "id":1,
                            "firstName":"Aleksandr",
                            "lastName":"Nedorezov",
                            "email": "nedorezov@own.space"
                        },
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/activities/2"
                            },
                            {
                                "rel":"author",
                                "href":"/users/1"
                            },
                            {
                                "rel":"authorThumbnail",
                                "href":"/users/1/profileThumbnail"
                            },
                            {
                                "rel":"board",
                                "href":"/boards/1"
                            }
                        ]
                    }
                ],
                "_links":[
                    {
                        "rel":"self",
                        "href":"/activities"
                    }
                ]
            }


# GET /boards/{boardId}/activities?from={from}&to={to}&limit={limit}&state={state}

If a `limit` count is given, no more than that many activity will be returned (but possibly less,
if the query itself yields less rows). Negative or equal 0 limit is the same as omitting the `limit` clause.

Parameters `from` and `to` represent the time bounds in milliseconds 
(between the wanted time and midnight, January 1, 1970 UTC).
If they are set, only activities made from time passed in `from` and to time passed in `to` will be returned.

If `state` parameter is set, only activities of with this state are returned, 
otherwise request returns activities with all possible states.
States can be `VALID`, `MERGED`, `RESTORED`, `DELETED`, and `INVALID`.

Usage of parameters `from`, `to`, `limit`, and `state` is not mandatory.

+ Request
    + Headers
    
                Accept: application/vnd.uberblik.activity+json;charset:UTF-8
                access-token : uywg87gw6gf6g468gf46g4f6g34f4f4


+ Response 200 (application/vnd.uberblik.activities+json)

    + Body
    
            {
                "activities":[
                    {
                        "type":"ElementRestored",
                        "published":1522347021470,
                        "displayText":"[Thu Mar 29 21:10:21 MSK 2018] Aleksandr restored element <6,2> to Welcome to OWN",
                        "details":{
                            "elementCaption":"this is a test element"
                        },
                        "state":"VALID",
                        "author":{
                            "id":1,
                            "firstName":"Aleksandr",
                            "lastName":"Nedorezov",
                            "email": "nedorezov@own.space"
                        },
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/activities/401"
                            },
                            {
                                "rel":"author",
                                "href":"/users/1"
                            },
                            {
                                "rel":"authorThumbnail",
                                "href":"/users/1/profileThumbnail"
                            },
                            {
                                "rel":"board",
                                "href":"/boards/1"
                            },
                            {
                                "rel":"element",
                                "href":"/boards/1/elements/1"
                            },
                            {
                                "rel":"elementThumbnail",
                                "href":"/boards/1/elements/1/thumbnail"
                            }
                        ]
                    },
                    {
                        "type":"ElementRemoved",
                        "published":1522343369668,
                        "displayText":"[Thu Mar 29 20:09:29 MSK 2018] Aleksandr removed element <3,2> from Welcome to OWN",
                        "details":{
                            "elementCaption":"this is a test element"
                        },
                        "state":"RESTORED",
                        "author":{
                            "id":1,
                            "firstName":"Aleksandr",
                            "lastName":"Nedorezov",
                            "email": "nedorezov@own.space"
                        },
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/activities/361"
                            },
                            {
                                "rel":"author",
                                "href":"/users/1"
                            },
                            {
                                "rel":"authorThumbnail",
                                "href":"/users/1/profileThumbnail"
                            },
                            {
                                "rel":"board",
                                "href":"/boards/1"
                            },
                            {
                                "rel":"element",
                                "href":"/boards/1/elements/1"
                            },
                            {
                                "rel":"elementThumbnail",
                                "href":"/boards/1/elements/1/thumbnail"
                            },
                            {
                                "rel":"restore",
                                "href":"/activities/361/restore"
                            },
                            {
                                "rel":"erase",
                                "href":"/boards/1/elements/1"
                            }
                        ]
                    },
                    {
                        "type":"FileCommented",
                        "published":1522061733704,
                        "displayText":"[Mon Mar 26 13:55:33 MSK 2018] Aleksandr commented a file awddaw to Welcome to OWN",
                        "details":{
                            "fileName":"камазазаза",
                            "fileType":"image/jpeg",
                            "comment":"awddaw"
                        },
                        "state":"VALID",
                        "author":{
                            "id":1,
                            "firstName":"Aleksandr",
                            "lastName":"Nedorezov",
                            "email": "nedorezov@own.space"
                        },
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/activities/223"
                            },
                            {
                                "rel":"author",
                                "href":"/users/1"
                            },
                            {
                                "rel":"authorThumbnail",
                                "href":"/users/1/profileThumbnail"
                            },
                            {
                                "rel":"file",
                                "href":"/boards/1/elements/1/files/1"
                            },
                            {
                                "rel":"fileThumbnail",
                                "href":"/boards/1/elements/1/files/1/thumbnail"
                            },
                            {
                                "rel":"element",
                                "href":"/boards/1/elements/1"
                            },
                            {
                                "rel":"board",
                                "href":"/boards/1"
                            },
                            {
                                "rel":"restore",
                                "href":"/activities/223/restore"
                            },
                            {
                                "rel":"erase",
                                "href":"/boards/1/elements/1/files/1/comments/223"
                            }
                        ]
                    },
                    {
                        "type":"FileAdded",
                        "published":1522061726516,
                        "displayText":"[Mon Mar 26 13:55:26 MSK 2018] Aleksandr added file <камазазаза> to element <3,2> to Welcome to OWN",
                        "details":{
                            "fileName":"камазазаза",
                            "fileType":"image/jpeg"
                        },
                        "state":"VALID",
                        "author":{
                            "id":1,
                            "firstName":"Aleksandr",
                            "lastName":"Nedorezov",
                            "email": "nedorezov@own.space"
                        },
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/activities/222"
                            },
                            {
                                "rel":"author",
                                "href":"/users/1"
                            },
                            {
                                "rel":"authorThumbnail",
                                "href":"/users/1/profileThumbnail"
                            },
                            {
                                "rel":"file",
                                "href":"/boards/1/elements/1/files/1"
                            },
                            {
                                "rel":"fileThumbnail",
                                "href":"/boards/1/elements/1/files/1/thumbnail"
                            },
                            {
                                "rel":"element",
                                "href":"/boards/1/elements/1"
                            },
                            {
                                "rel":"board",
                                "href":"/boards/1"
                            }
                        ]
                    },
                    {
                        "type":"UserJoinedBoard",
                        "published":1520860463514,
                        "displayText":"[Mon Mar 12 16:14:23 MSK 2018] Aleksandr joined the board Welcome to OWN",
                        "details":{
                            "boardName":"Welcome to OWN"
                        },
                        "state":"VALID",
                        "author":{
                            "id":1,
                            "firstName":"Aleksandr",
                            "lastName":"Nedorezov",
                            "email": "nedorezov@own.space"
                        },
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/activities/2"
                            },
                            {
                                "rel":"author",
                                "href":"/users/1"
                            },
                            {
                                "rel":"authorThumbnail",
                                "href":"/users/1/profileThumbnail"
                            },
                            {
                                "rel":"board",
                                "href":"/boards/1"
                            }
                        ]
                    }
                ],
                "_links":[
                    {
                        "rel":"self",
                        "href":"/boards/1/activities"
                    }
                ]
            }

# GET /boards/{boardId}/activities/count

+ Request
    + Headers
    
                Accept: application/vnd.uberblik.activitiesCount+json;charset:UTF-8
                access-token : uywg87gw6gf6g468gf46g4f6g34f4f4


+ Response 200 (application/vnd.uberblik.activitiesCount+json)

    + Body

            {
                "activitiesCount": 109
            }

# GET /activities/{activityId}

+ Request
    
    + Headers
    
            Accept: application/vnd.uberblik.activity+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4


+ Response 200 (application/vnd.uberblik.activity+json)

    + Body
    
            {
                "activity":{
                    "type":"UserJoinedBoard",
                    "published":1520860463514,
                    "displayText":"[Mon Mar 12 16:14:23 MSK 2018] Aleksandr joined the board Welcome to OWN",
                    "details":{
                        "boardName":"Welcome to OWN"
                    },
                    "state":"VALID",
                    "author":{
                        "id":1,
                        "firstName":"Aleksandr",
                        "lastName":"Nedorezov",
                        "email": "nedorezov@own.space"
                    },
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/activities/2"
                        },
                        {
                            "rel":"author",
                            "href":"/users/1"
                        },
                        {
                            "rel":"authorThumbnail",
                            "href":"/users/1/profileThumbnail"
                        },
                        {
                            "rel":"board",
                            "href":"/boards/1"
                        }
                    ]
                }
            }

# POST /activities/{activityId}/restore

+ Request
    
    + Headers
    
            Accept: application/vnd.uberblik.activity+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

    + Body
    
            {
                "posX": 1,
                "posY": 1
            }


+ Response 201 (application/vnd.uberblik.element+json)

    + Body
    
            {
                "element": {
                    "posX":"1", 
                    "posY":"1", 
                    "sizeX":"1", 
                    "sizeY":"1", 
                    "type":"MultiInput",
                    "caption" : "this is a test element",
                    "_links":
                    [
                        { "rel": "self", "href": "/GET boards/211/elements/6327654" },
                        { "rel" : "files", "href" : "/boards/211/elements/6327654/files" }
                    ]
                }
            }       

            
# Group Archived elements and files

Archived elements/files are elements/files that were previously deleted from a board. 

### Deleting archived elements or files

Deleting archived elements or files is a non reversible operation. An element or file that is deleted from the 
archive is gone forever. Also, deleting an archived element also deletes all files 
for that element.

Common http codes returned by operations on archived elements or files:

+ `200` when sucessfully retrieved or deleted an archived element or file
+ `403` returned if the token is expired, invalid or not found


## GET /archive/boards/{boardId}/elements

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.archivedElements+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4


+ Response 200(application/vnd.uberblik.archivedElements+json)

    + Body
    
            {
                 "archivedElements": [
                    {
                        "caption": "",
                        "type": "MultiInput",
                        "sizeX": 1,
                        "sizeY": 1,
                        "posX": 5,
                        "posY": 2,
                        "_links": [
                            {
                                "rel": "self",
                                "href": "/boards/1/elements/41"
                            }
                        ]
                    },
                    {
                        "caption": "this is a test element",
                        "type": "MultiInput",
                        "sizeX": 1,
                        "sizeY": 1,
                        "posX": 5,
                        "posY": 4,
                        "_links": [
                            {
                                "rel": "self",
                                "href": "/boards/1/elements/62"
                            }
                        ]
                    }
                ], "_links": [
                    {
                        "rel": "self",
                        "href": "/archive/boards/1/elements"
                    }
                ]
            }
            
## GET /archive/boards/{boardId}/elements/{elementId}

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.archivedElement+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200(application/vnd.uberblik.archivedElement+json)

    + Body
            
            {
                "archivedElement": {
                    "caption": "",
                    "type": "MultiInput",
                    "sizeX": 1,
                    "sizeY": 1,
                    "posX": 5,
                    "posY": 2,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/1/elements/41"
                        },
                        {
                            "rel": "archivedFiles",
                            "href": "/archive/boards/1/elements/41/files"
                        }
                    ]
                }
            }

## DELETE /archive/boards/{boardId}/elements/{elementId}

+ Request 
    + Headers
    
            Accept: */*
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4


+ Response 200 ()

## DELETE /archive/boards/{boardId}/elements/{elementId}/files/{fileId}

+ Request 
    + Headers
    
            Accept: */*
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 ()

## GET /archive/boards/{boardId}/files

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.archivedFiles+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4


+ Response 200(application/vnd.uberblik.archivedFiles+json)

    + Body
            
            {"archivedFiles": [
                {
                    "name": "0002.jpg",
                    "fileType": "image/jpeg",
                    "index": 0,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/1/elements/1/files/1"
                        },
                        {
                            "rel": "element",
                            "href": "/boards/1/elements/1"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/1/elements/1/files/1/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/1/elements/1/files/1/boardThumbnail"
                        },
                        {
                            "rel": "preview",
                            "href": "/boards/1/elements/1/files/1/preview"
                        }
                    ]
                },
                {
                    "name": "flickr1.jpg",
                    "fileType": "image/jpeg",
                    "index": 0,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/1/elements/21/files/21"
                        },
                        {
                            "rel": "element",
                            "href": "/boards/1/elements/21"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/1/elements/21/files/21/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/1/elements/21/files/21/boardThumbnail"
                        },
                        {
                            "rel": "preview",
                            "href": "/boards/1/elements/21/files/21/preview"
                        }
                    ]
                }
            ], "_links": [
                {
                    "rel": "self",
                    "href": "/archive/boards/1/files"
                }
            ]}

## GET /archive/boards/{boardId}/elements/{elementId}/files

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.user+archivedFiles;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 (application/vnd.uberblik.archivedFiles+json)

    + Body
            
            {"archivedFiles": [
                {
                    "name": "MyPdfFile.pdf",
                    "fileType": "application/pdf",
                    
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/1/elements/41/files/41"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/1/elements/41/files/41/thumbnail"
                        },
                        {
                            "rel": "boardThumbnail",
                            "href": "/boards/1/elements/41/files/41/boardThumbnail"
                        },
                        {
                            "rel": "preview",
                            "href": "/boards/1/elements/41/files/41/preview"
                        }
                    ]
                }
            ], "_links": [
                {
                    "rel": "self",
                    "href": "/archive/boards/1/elements/41/files"
                }
            ]}

# Group Board posts

Common http codes returned by operations on board posts:

+ `200` when sucessfully retrieved a board post
+ `403` returned if the token is expired, invalid or not found


## GET /boards/{boardId}/posts/{postId}

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.post+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4


+ Response 200 (application/vnd.uberblik.post+json)

    + Body
    
            {
                "post":
                {
                    "message":"Post message",
                    "created":1395070480487,
                    "_links":
                    [
                        {"rel":"self","href":"/boards/1/posts/21"},
                        {"rel":"author","href":"/users/1"}
                    ]
                }
            }

## POST /boards/{id}/posts

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.post+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

    + Body

            {
                "post": 
                {
                    "message": "Post message"
                }
            }
            
+ Response 201 (application/vnd.uberblik.post+json)

    + Body
    
            {
                "post":
                {
                    "message":"Post message",
                    "created":1395070480487,
                    "_links":[
                        {"rel":"self","href":"/boards/1/posts/21"},
                        {"rel":"author","href":"/users/1"}
                    ]
                }
            }
        

## DELETE /boards/{boardId}/posts/{postId}

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.post+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4


+ Response 200

# Group Live updates

Live updates provide clients with near real-time events about changes to the resources 
that the current user has access to. In order to avoid polling, we use web sockets for 
this type of communication. <br><br>
Since most clients, especially web browsers, cannot add custom headers when establishing 
a web sockets connection, the call to the `/opensocket` endpoint has to pass the access 
token as a parameter in the URL. Since the call effectively switches the protocol from 
HTTPS to WSS, the response code in the success case is 101.<br><br>
Once the client has establshed the connection to the live update socket, the server will 
send custom JSON objects to the connected clients as soon as things are changed on the 
respective resources.<br><br>
Some live updates carry a representation of the whole board to enable the client to stay in-sync. It has following form: <br>
   "board": ["posx,posy,sizex,sizey,elementPath,caption,filecount,topfileid"]<br>
The topfileid is the href that sits on top of the file, with the highest index, 
which provides the thumbnail for the element. Thumbnail, caption and topfileid can be empty.
<br><br>
These custom objects are identified by their content type attribute. The following 
objects are supported:

| contentType <br>application/vnd.uberblik. +            | expected client action  |
| :------------------------------------------------------|:------------------------|
| liveUpdateBoardCreated                                 | client should load the new board |
| liveUpdateBoardDeleted                                 | client should remove the board |
| liveUpdateBoardOverviewChanged+json                    | client should update  the thumbnail of the board |
| liveUpdateElementMoved+json                            | client should move the element from oldPosition to newPosition |
| liveUpdateElementResized+json                          | client should re-render the element with the new size |
| liveUpdateMemberInvitedToBoard                         | client should add invited member to the list of boards users, as a "pending" member (i.e. invitation was not accepted yet) |
| liveUpdateUserJoinedBoard                              | client should add joined user to the list of boards users |
| liveUpdateUserLeftBoard                                | cliend should remove the user who left board from the list of boards users |
| liveUpdateBoardNameEdited                              | client should update boards name |
| liveUpdateBoardInvitationModelChanged                  | client should update boards invitation model |
| liveUpdateElementAdded+json                            | client should display the new element |
| liveUpdateElementMerged+json                           | client should reload the element as it was merged with another one |
| liveUpdateElementDeleted+json                          | client should remove the element from the board |
| liveUpdateElementPermanentlyDeleted+json               | client should delete all elements data if it was cached |
| liveUpdateFileAdded+json                               | client should re-render the element with the new file added |
| liveUpdateElementFileDeleted+json                      | client should remove the file from the specified element |
| liveUpdateElementCaptionEdited+json                    | client should replace the old caption with the new one |
| liveUpdateElementFileListUpdated+json                  | client should update the list of files for the specified element |
| liveUpdateElementFilePermanentlyDeleted+json           | client should delete all files data if it was cached |
| LiveUpdateFileCommentAdded                             | client should load the added comment and add it to file |
| LiveUpdateFileCommentDeleted                           | client should remove the comment |
| liveUpdateUserNameEdited                               | client should update first name, last name, and display name of the user |
| liveUpdateUserProfileThumbnailChanged                  | client should update users profile thumbnail (avatar) |
| liveUpdateUserLocaleChanged                            | client should update users locale |
| liveUpdateUserDailyActivityDigestChanged               | client should update daily activity digest setting of the user |
| liveUpdatePostAdded                                    | client should load new board post |
| liveUpdatePostDeleted                                  | client should remove board post |
| liveUpdateActivitiesUpdated+json                       | client should reload the activities for either the current board or all boards |
| liveUpdatePingMessage+json                             | client should store the "time" parameter and handle timeout conditions |
| liveUpdateBoardFreeSpaceUpdated                        | client should update free space of the board |
| liveUpdateSync+json                                    | client should compare his timestamps and synchronize if necessary |
| LiveUpdateElementsAgentTaskEdited                      | client should update elements forms & files |
| LiveUpdateBoardAssignedToAnOrganization                | client should update organizations thumbnail |
| LiveUpdateOrganizationCreated                          | client should add created organization to the list of users organizations |
| LiveUpdateOrganizationDeleted                          | client should remove all users from organization & delete it |
| LiveUpdateOrganizationUserAdded                        | client should add specified user to the list of organization members |
| LiveUpdateOrganizationUserDeleted                      | client should remove specified user from the list of organization members, and remove all organization boards for the deleted user. |
| LiveUpdateOrganizationUserStatusChanged                | client should update user membersip status in the list of organization members |
| LiveUpdateOrganizationProfileThumbnailChanged          | client should update organizations profile thumbnail (avatar) |
| LiveUpdateOrganizationNameChanged                      | client should update organizations name |
| LiveUpdateOrganizationLegalNameChanged                 | client should update organizations legal name |
| LiveUpdateOrganizationBillingAddressChanged            | client should update organizations billing address |
| LiveUpdateOrganizationCityChanged                      | client should update organizations city |
| LiveUpdateOrganizationStateChanged                     | client should update organizations state |
| LiveUpdateOrganizationCountryChanged                   | client should update organizations country |
| LiveUpdateOrganizationZipCodeChanged                   | cliend should update organizations zip code |
| LiveUpdateOrganizationVatIdChanged                     | client should update organizations vatId |
| LiveUpdateAgentTaskElementCreated                      | client should save a connection between agent task and element |
| LiveUpdateAgentTaskElementDeleted                      | client should delete a connection between agent task and element |
| LiveUpdateAgentTaskElementAnswersSaved                 | client should save answers to agent task related to element |
| LiveUpdateUserAgentSubscriptionPerformedQueriesUpdated | client should update performedQueries number for the given userAgentSubscription |
| LiveUpdateUsersAgentSubscriptionUpdated                | client should remove all user agent subscriptions with given agentDataId and get a new active one, if provided |
| LiveUpdateOrganizationsAgentSubscriptionUpdated        | client should remove all organization agent subscriptions with given agentDataId and get a new active one, if provided |
| LiveUpdateUserViewedAllFilesInElement                  | client should set `viewed` parameter to `true` for all files in element with id=`elementId` |

The following live updates are **DEPRECATED**, and will be removed from API shortly. You should avoid using them.

| contentType <br>application/vnd.uberblik. + | expected client action  |
| :--------------------------------------------|:------------------------|
| liveUpdateUserListChanged+json               | **DEPRECATED**: Use liveUpdateUserJoinedBoard, and liveUpdateUserLeftBoard instead. Client should update  user list on the board |
| liveUpdateFileCommented+json                 | **DEPRECATED**: Use either LiveUpdateFileCommentAdded for monitoring additions of files comments, or LiveUpdateFileCommentDeleted for monitoring deletions of files comments. <br /> <br /> client should update comments of a file in the lightbox. |


Below are examples for each of the content types mentioned in the table above:

```
{
    "contentType":"application/vnd.uberblik.liveUpdateBoardCreated+json",
    "boardId":481
}
```

```
{
    "contentType":"application/vnd.uberblik.liveUpdateBoardDeleted+json",
    "path":"/boards/481"
}
```

```
{
    "contentType":"application/vnd.uberblik.liveUpdateBoardOverviewChanged+json",
    "path":"/boards/1"
}
```

```
{
    "contentType":"application/vnd.uberblik.liveUpdateElementMoved+json",
    "path":"/boards/1/elements/561",
    "newPosX":3,
    "newPosY":2,
    "oldPosX":2,
    "oldPosY":2
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateElementResized+json",
    "path": "/boards/1/elements/561",
    "newSizeX": 2,
    "newSizeY": 2,
    "oldSizeX": 1,
    "oldSizeY": 1
}
```

```
{
    "contentType":"application/vnd.uberblik.liveUpdateMemberInvitedToBoard+json",
    "boardId":301,
    "inviterId":1,
    "inviteeId":121,
    "invitationId":161
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateUserJoinedBoard+json",
    "boardId": 1,
    "userId": 41
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateUserLeftBoard+json",
    "boardId": 1,
    "userId": 41
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateBoardNameEdited+json",
    "boardId": 1,
    "newBoardName": "1"
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateBoardInvitationModelChanged+json",
    "boardId": 1,
    "newBoardInvitationModel": "ADMIN_ONLY"
}
```

Possible invitation models are: `MEMBERS_ALLOWED`, and `ADMIN_ONLY`.

```
{
    "contentType": "application/vnd.uberblik.liveUpdateElementAdded+json",
    "path": "/boards/1/elements/562"
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateElementMerged+json",
    "targetPath": "/boards/1/elements/561",
    "mergedPath": "/boards/1/elements/562"
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateElementDeleted+json",
    "path": "/boards/1/elements/562",
    "posX": 3,
    "posY": 1
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateElementPermanentlyDeleted+json",
    "path": "/boards/1/elements/562",
    "board": "/boards/1"
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateFileAdded+json",
    "path": "/boards/1/elements/1/files/21",
    "elementFilesCount": 4
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateFileDeleted+json",
    "path": "/boards/1/elements/1/files/41",
    "elementFilesCount": 3
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateElementCaptionEdited+json",
    "path": "/boards/1/elements/61",
    "newCaption": "awdawdawdddw"
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateElementFileListUpdated+json",
    "path": "/boards/1/elements/61"
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateElementFilePermanentlyDeleted+json",
    "path": "/boards/1/elements/564/files/182",
    "board": "/boards/1"
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateFileCommentAdded+json",
    "path": "/boards/1/elements/1/files/303/comments/2536"
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateFileCommentDeleted+json",
    "path": "/boards/1/elements/1/files/303/comments/2536"
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateUserNameEdited+json",
    "userId": 1,
    "newFirstName": "Aleksandr",
    "newLastName": "Nedorezov",
    "newDisplayName": "Aleksandr Nedorezov"
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateUserProfileThumbnailChanged+json",
    "userId": 3671
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateUserLocaleChanged+json",
    "userId": 1,
    "newLocale": "en"
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateUserDailyActivityDigestChanged+json",
    "userId": 1,
    "dailyActivityDigest": false
}
```

```
{
    "contentType":"application/vnd.uberblik.liveUpdatePostAdded+json",
    "postId":81,
    "boardId":1,
    "activityDisplayText":"Aleksandr posted some text to Welcome to OWN"
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdatePostDeleted+json",
    "postId": 281,
    "boardId": 1
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateActivitiesUpdated+json",
    "path": "/boards/1",
    "affectsAllEntries": false
}
```

```
{
    "contentType" : "application/vnd.uberblik.liveUpdatePingMessage+json"
    "time":1396859222959,
    "connectedClients":["2: EdF/ZbsdDZXRA6+c0ku6PwmpjNFzd4YXPK8r+ModcUIxn3Sf/T2nOR1o89GCnXrn"]
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateBoardFreeSpaceUpdated+json",
    "boardId": 1,
    "freeSpace": 296841801
}
```

```
{
    "contentType" : "liveUpdateSync+json",
    "board": "boards/999",
    "timestamp" : 1234560000,
    "history": [1234550000,1234540000,1234530000,1234520000,1234510000]

}
```

```
{
    "contentType":"application/vnd.uberblik.liveUpdateElementsAgentTaskEdited+json",
    "path":"/boards/1/elements/382",
    "newAgentTaskIdOrNull":21
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateBoardAssignedToAnOrganization+json",
    "boardId": 261,
    "organizationId": 81
}
```

```
{
  "contentType": "application/vnd.uberblik.liveUpdateOrganizationCreated+json",
  "organizationId": 101
}
```

```
{
  "contentType": "application/vnd.uberblik.liveUpdateOrganizationDeleted+json",
  "organizationId": 41
}
```

```
{
  "contentType": "application/vnd.uberblik.liveUpdateOrganizationUserAdded+json",
  "organizationId": 42,
  "userId": 21,
  "organizationUserStatus": "MEMBER"
}
```

```
{
  "contentType": "application/vnd.uberblik.liveUpdateOrganizationUserDeleted+json",
  "organizationId": 42,
  "userId": 21
}
```

```
{
  "contentType": "application/vnd.uberblik.liveUpdateOrganizationUserStatusChanged+json",
  "organizationId": 42,
  "userId": 21,
  "organizationUserStatus": "ADMINISTRATOR"
}
```

```
{
  "contentType": "application/vnd.uberblik.liveUpdateOrganizationProfileThumbnailChanged+json",
  "organizationId": 42
}
```

```
{
  "contentType": "application/vnd.uberblik.liveUpdateOrganizationNameChanged+json",
  "organizationId": 42,
  "name": "Name"
}
```

```
{
  "contentType": "application/vnd.uberblik.liveUpdateOrganizationLegalNameChanged+json",
  "organizationId": 42,
  "legalName": "Ururu, Inc."
}
```

```
{
  "contentType": "application/vnd.uberblik.liveUpdateOrganizationBillingAddressChanged+json",
  "organizationId": 42,
  "billingAddress": "Sportivnaya, 101, 102"
}
```

```
{
  "contentType": "application/vnd.uberblik.liveUpdateOrganizationCityChanged+json",
  "organizationId": 42,
  "city": "Innopolis"
}
```

```
{
  "contentType": "application/vnd.uberblik.liveUpdateOrganizationStateChanged+json",
  "organizationId": 42,
  "state": "Texas"
}
```

```
{
  "contentType": "application/vnd.uberblik.liveUpdateOrganizationCountryChanged+json",
  "organizationId": 42,
  "country": "Russian Federation"
}
```

```
{
  "contentType": "application/vnd.uberblik.liveUpdateOrganizationZipCodeChanged+json",
  "organizationId": 101,
  "zipCode": "012345678l9"
}
```

```
{
  "contentType": "application/vnd.uberblik.liveUpdateOrganizationVatIdChanged+json",
  "organizationId": 42,
  "vatId": "1234567890"
}
```

```
{
    "contentType":"application/vnd.uberblik.liveUpdateAgentTaskElementCreated+json",
    "agentDataId":61,
    "agentTaskId":161,
    "boardId":1,
    "elementId":101
}
```

```
{
    "contentType":"application/vnd.uberblik.liveUpdateAgentTaskElementDeleted+json",
    "agentDataId":61,
    "agentTaskId":161,
    "boardId":1,
    "elementId":101
}
```

```
{
    "contentType":"application/vnd.uberblik.liveUpdateAgentTaskElementAnswersSaved+json",
    "agentDataId":61,
    "agentTaskId":161,
    "boardId":1,
    "elementId":101,
    "agentQueryId":103
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateUserAgentSubscriptionPerformedQueriesUpdated+json",
    "userAgentSubscriptionId": 101,
    "performedQueries": 4
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateUsersAgentSubscriptionUpdated+json",
    "userId": 1,
    "agentDataId": 61,
    "activeUserAgentSubscriptionId": 181
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateOrganizationsAgentSubscriptionUpdated+json",
    "organizationId": 1,
    "agentDataId": 61,
    "activeOrganizationAgentSubscriptionId": 181
}
```

```
{
    "contentType": "application/vnd.uberblik.liveUpdateUserViewedAllFilesInElement+json",
    "userId": 1,
    "boardId": 1,
    "elementId": 1
}
```
-------------
Deprecated live updates
-------------

```
{
    "contentType" : "application/vnd.uberblik.liveUpdateBoardUserListChanged+json",
    "path" : "/boards/1"
}
```

```
{
    "contentType" : "application/vnd.uberblik.liveUpdateFileCommented+json",
    "path" : "/boards/1/elements/1/file/1",
    "board" : "/boards/1"
}
```


## GET /opensocket{?token}

+ Response 101

# Group Organizations

Users can create organizations to brand their boards, regulate membership & assignment of boards to organizations.

The requests below contain several enums in their body, such as:
organizationStatus: `ACTIVE`, `INACTIVE`
organizationUserStatus: `MEMBER`, `ADMINISTRATOR`, `CREATOR`

`CREATOR` has the same permissions as `ADMINISTRATOR`. The role differs only in that `CREATOR` had created an organization he is a creator of, and administrator did not.

All organization users can assign a board, whether at its creation, or already existing one, to an organization, and get access to the organizations boards,
but only `ADMINISTRATOR`s or a `CREATOR` can edit or delete organization, add users to the organization, change organization users status, or delete users from the organization.

(see section `/boards` for assignment of boards to organizations during their creation)

## GET /organizations

Returns organizations of the user whose access token was sent in the request.

`organizationUserStatus` field shows status of user who makes the request in the organization in question.

+ Request 
    + Headers
    
            Accept: application/vnd.uberblik.organizations+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4

+ Response 200 (application/vnd.uberblik.organizations+json)

    + Body
    
            {
              "organizations": [
                {
                  "id": 101,
                  "name": "Hogwarts",
                  "status": "ACTIVE",
                  "legalName": "Hogwarts school of witchcraft and wizadry",
                  "billingAddress": "Your owl fill find us",
                  "city": "1",
                  "state": "1",
                  "country": "United Kingdom of Britain and Northern Ireland",
                  "zipCode": "012345678l9",
                  "vatId": "11111111111111111",
                  "organizationUserStatus": "ADMINISTRATOR",
                  "_links": [
                    {
                      "rel": "self",
                      "href": "/organizations/101"
                    },
                    {
                      "rel": "thumbnail",
                      "href": "/organizations/101/thumbnail"
                    }
                  ]
                },
                {
                  "id": 42,
                  "name": "Name",
                  "status": "ACTIVE",
                  "legalName": "11",
                  "billingAddress": "Sportivnaya, 101, 102",
                  "city": "Innopolis",
                  "state": "Texas",
                  "country": "Russian Federation",
                  "zipCode": null,
                  "vatId": "1234567890",
                  "organizationUserStatus": "MEMBER",
                  "_links": [
                    {
                      "rel": "self",
                      "href": "/organizations/42"
                    },
                    {
                      "rel": "thumbnail",
                      "href": "/organizations/42/thumbnail"
                    }
                  ]
                }
              ],
              "_links": [
                {
                  "rel": "self",
                  "href": "/organizations"
                }
              ]
            }


## POST /organizations

Note that this `POST` request also returns `organizationUser` link, which contains an id of organizations creator.

Only `name` field is obligatory.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.organization+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
    + Body
    
            {
              "organization": {
                "name": "Hogwarts",
                "legalName": "Hogwarts school of witchcraft and wizadry",
                "billingAddress": "Your owl fill find us",
                "city": "London",
                "state": "Madness",
                "country": "United Kingdom of Britain and Northern Ireland",
                "zipCode": "420500"
                "vatId": "11111111111111111"
              }
            }
            
+ Response 200 (application/vnd.uberblik.organization+json)

    + Body
                
            {
              "organization": {
                "id": 122,
                "name": "Hogwarts",
                "status": "ACTIVE",
                "legalName": "Hogwarts school of witchcraft and wizadry",
                "billingAddress": "Your owl fill find us",
                "city": "London",
                "state": "Madness",
                "country": "United Kingdom of Britain and Northern Ireland",
                "zipCode": "420500",
                "vatId": "11111111111111111",
                "_links": [
                  {
                    "rel": "self",
                    "href": "/organizations/122"
                  },
                  {
                    "rel": "organizationUser",
                    "href": "/organizations/122/users/1"
                  },
                  {
                    "rel": "thumbnail",
                    "href": "/organizations/122/thumbnail"
                  }
                ]
              }
            }

## GET /organizations/{organizationId}

If user who makes a request is not a member of organization with id `organizationId` 
he/she would only get base data (`name`, `status`).

If user who makes a request is a member of organization, 
he/she will get data about his/hers status in the organization via `organizationUserStatus` field.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.organization+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.organization+json)

    + Body
                
            {
              "organization": {
                "id": 122,
                "name": "Hogwarts",
                "status": "ACTIVE",
                "legalName": "Hogwarts school of witchcraft and wizadry",
                "billingAddress": "Your owl fill find us",
                "city": "London",
                "state": "Madness",
                "country": "United Kingdom of Britain and Northern Ireland",
                "zipCode": "420500",
                "vatId": "11111111111111111",
                "organizationUserStatus": "ADMINISTRATOR",
                "_links": [
                  {
                    "rel": "self",
                    "href": "/organizations/122"
                  },
                  {
                    "rel": "organizationUser",
                    "href": "/organizations/122/users/1"
                  },
                  {
                    "rel": "thumbnail",
                    "href": "/organizations/122/thumbnail"
                  }
                ]
              }
            }

## PUT /organizations/{organizationId}

JSON with any of the fields given in requests body (not necessary all of them), 
will also be a valid body for this request. 
Therefore, in the request body, you may only pass those user parameters, which you want to modify.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.organization+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
    + Body

            {
              "organization": {
                "name": "Narnia",
                "legalName": "Narnia school of witchcraft and wizadry",
                "billingAddress": "Your centaur fill find us",
                "country": "United Episodes of Monty Python",
                "zipCode": "123456",
                "vatId": "244234234234234"
              }
            }
            
+ Response 200 (application/vnd.uberblik.organization+json)

    + Body
    
            {
              "organization": {
                "id": 101,
                "name": "Narnia",
                "status": "ACTIVE",
                "legalName": "Narnia school of witchcraft and wizadry",
                "billingAddress": "Your centaur fill find us",
                "city": "1",
                "state": "1",
                "country": "United Episodes of Monty Python",
                "zipCode": "123456",
                "vatId": "244234234234234",
                "_links": [
                  {
                    "rel": "self",
                    "href": "/organizations/101"
                  },
                  {
                    "rel": "thumbnail",
                    "href": "/organizations/101/thumbnail"
                  }
                ]
              }
            }

## DELETE /organizations/{organizationId}

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.organization+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200


## POST /organizations/{organizationId}/users/{userId}

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.organizationUser+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
    + Body
    
            {
                "organizationUser": {
                    "organizationUserStatus": "ADMINISTRATOR"
                }
            }
            
+ Response 200 (application/vnd.uberblik.organizationUser+json)

    + Body
                
            {
                "organizationUser": {
                    "organization": {
                        "name": "A Cool Organization",
                        "status": "ACTIVE"
                    },
                    "groklandUser": {
                        "email": "abc@test.own.space",
                        "firstName": "Test Agent",
                        "lastName": "Agent",
                        "displayName": "Test Agent",
                        "locale": "en",
                        "dailyActivityDigest": true,
                        "status": "PENDING"
                    },
                    "organizationUserStatus": "ADMINISTRATOR",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/organizations/1/users/22/organizationusers"
                        }
                    ]
                }
            }
            
+ Responce 403            
            
+ Responce 404

## GET /organizations/{organizationId}/users/{userId}

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.organizationUser+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.organizationUser+json)

    + Body
                
            {
                "organizationUser": {
                    "organization": {
                        "name": "A Cool Organization",
                        "status": "ACTIVE"
                    },
                    "groklandUser": {
                        "email": "abc@test.own.space",
                        "firstName": "Test Agent",
                        "lastName": "Agent",
                        "displayName": "Test Agent",
                        "locale": "en",
                        "dailyActivityDigest": true,
                        "status": "PENDING"
                    },
                    "organizationUserStatus": "ADMINISTRATOR",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/organizations/1/users/22/organizationusers"
                        }
                    ]
                }
            }

## PUT /organizations/{organizationId}/users/{userId}

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.organizationUser+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
    + Body
    
            {
                "organizationUser": {
                    "organizationUserStatus": "MEMBER"
                }
            }
            
+ Response 200 (application/vnd.uberblik.organizationUser+json)

    + Body
                
            {
                "organizationUser": {
                    "organization": {
                        "name": "A Cool Organization",
                        "status": "ACTIVE"
                    },
                    "groklandUser": {
                        "email": "abc@test.own.space",
                        "firstName": "Test Agent",
                        "lastName": "Agent",
                        "displayName": "Test Agent",
                        "locale": "en",
                        "dailyActivityDigest": true,
                        "status": "PENDING"
                    },
                    "organizationUserStatus": "MEMBER",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/organizations/1/users/22/organizationusers"
                        }
                    ]
                }
            }

## DELETE /organizations/{organizationId}/users/{userId}

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.organizationUser+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200

## POST /organizations/{organizationId}/users

Returns `400` error with `User with email email@domain.com does not exist in the system.` x-uberblik-error message if user with `email@domain.com` does not exist in the system.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.organizationUser+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
    + Body
    
            {
              "organizationUser": {
                "groklandUser": {
                  "email": "demomailbot@test.own.space"
                },
                "organizationUserStatus": "ADMINISTRATOR"
              }
            }
            
+ Response 200 (application/vnd.uberblik.organizationUser+json)

    + Body
 
            {
                "organizationUser": {
                    "organization": {
                        "name": "Hogwarts",
                        "status": "ACTIVE",
                        "legalName": "Hogwarts school of witchcraft and wizadry",
                        "billingAddress": "Your owl fill find us",
                        "country": "United Kingdom of Britain and Northern Ireland",
                        "vatId": "11111111111111111"
                    },
                    "groklandUser": {
                        "email": "demoMailbot@test.own.space",
                        "firstName": "Demonstrational",
                        "lastName": "Mailbot",
                        "displayName": "Demonstrational",
                        "locale": "en",
                        "dailyActivityDigest": true,
                        "status": "ACTIVE"
                    },
                    "organizationUserStatus": "ADMINISTRATOR",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/organizations/2/users/41"
                        }
                    ]
                }
            }

+ Responce 400

+ Responce 403            
            
+ Responce 404

## GET /organizations/{organizationId}/users

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.organizationUsers+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.organizationUsers+json)

    + Body
                
            {
                "organizationUsers": [
                    {
                        "organizationUserStatus": "ADMINISTRATOR",
                        "_links": [
                            {
                                "rel": "Users DisplayName",
                                "href": "/users/21"
                            }
                        ]
                    },
                    {
                        "organizationUserStatus": "CREATOR",
                        "_links": [
                            {
                                "rel": "Aleksandr Nedorezov",
                                "href": "/users/1"
                            }
                        ]
                    }
                ],
                "_links": [
                    {
                        "rel": "self",
                        "href": "/organizations/2/users"
                    }
                ]
            }

## PUT /organizations/{organizationId}/boards/{boardId}

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.board+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.board+json)

    + Body
                            
            {
                "board": {
                    "name": "Welcome to OWN",
                    "sizeX": 7,
                    "sizeY": 9,
                    "lastModified": 1512989715152,
                    "invitationModel": "MEMBERS_ALLOWED",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/boards/1"
                        },
                        {
                            "rel": "elements",
                            "href": "/boards/1/elements"
                        },
                        {
                            "rel": "archivedElements",
                            "href": "/archive/boards/1/elements"
                        },
                        {
                            "rel": "archivedFiles",
                            "href": "/archive/boards/1/files"
                        },
                        {
                            "rel": "users",
                            "href": "/boards/1/users"
                        },
                        {
                            "rel": "owner",
                            "href": "/users/1"
                        },
                        {
                            "rel": "activities",
                            "href": "/boards/1/activities"
                        },
                        {
                            "rel": "thumbnail",
                            "href": "/boards/1/thumbnail"
                        },
                        {
                            "rel": "posts",
                            "href": "/boards/1/posts"
                        },
                        {
                            "rel": "invitedUsers",
                            "href": "/boards/1/invitedUsers"
                        },
                        {
                            "rel": "quota",
                            "href": "/boards/1/quota"
                        },
                        {
                            "rel": "invitations",
                            "href": "/invitations"
                        },
                        {
                            "rel": "organizations",
                            "href": "/organizations"
                        },
                        {
                            "rel": "organization",
                            "href": "/organizations/1"
                        }
                    ]
                }
            }

## GET /organizations/{organizationId}/boards?limit={limit}&offset={offset}&order={order}

Gets a limited number of boards (as passed in limit query parameter) 
of an organization with id=organizationId (if a user whose access token was sent with request, 
is a member of this organization), skipping several (as passed in offset query parameter) 
boards before beginning the return of boards.

If a `limit` count is given, no more than that many rows will be returned (but possibly less,
if the query itself yields less rows). Negative or equal 0 limit is the same as omitting the `limit` clause.

Parameter `offset` says to skip that many rows before beginning to return rows. 
`offset` <=0 is the same as omitting the `offset` clause. If both `offset` and `limit` appear 
then `offset` rows are skipped before starting to count the LIMIT rows that are returned.

`order` parameter repsesents the order in which boards will be returned.
By default (if the `order` parameter were not passed) boards are returned sorted the time of last modification made on it in descending order (`limit=lastmodified`).
If you want to get boards sorted by board ids in descending order, use `order=boardid`.
Only `boardid` and `lastmodified` are valid values for the `order` parameter. If something else is passed,
`lastmodified` value will be set.

+ Request 

    + Headers
    
            Accept: application/vnd.uberblik.boards+json;charset:UTF-8

+ Response 200 (application/vnd.uberblik.boards+json)

    + Body
    
            {
                "boards":[
                    {
                        "rel":"Demo Board Name",
                        "href":"/boards/281"
                    },
                    {
                        "rel":"testboard1",
                        "href":"/boards/261"
                    },
                    {
                        "rel":"Welcome to OWN",
                        "href":"/boards/1"
                    }
                ]
            }

## Group Organizations thumbnails

Organization thumbnails (and all other image resources) are not protected. Often, the path to these
images is injected into the HTML code, therefore no custom headers can be applied to the 
request.<br>
Common http codes returned by operations on board thumbnails:

+ `200` when sucessfully retrieved a thumbnail


## GET /organizations/{organizationId}/thumbnail

+ Request
    + Headers
    
                Accept: image/jpeg


+ Response 200 (image/jpeg)
    
                2345f13463gg4nbbfgfbg3...

                
## PUT /organizations/{organizationId}/thumbnail

+ Request
    + Headers
    
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4


+ Response 200


# Group Agents Data

Entity AgentData stores unique identificators of agents, agents descriptions, salaries 
(cost for a period specified by `subscriptionInterval` and `subscriptionIntervalCount` fields), 
capacities (# of tasks performed in a period specified by 
`subscriptionInterval` and `subscriptionIntervalCount` fields), status of agent, 
which can be: `ACTIVE`, `BEING_TESTED`, and `INACTIVE`,
and agents `greetingMessage`, which is posted to the board when agent is invited to it.

## GET /agentdata

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentData+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.agentsData+json)

    + Body
    
            {
                "agentsData": [
                    {
                        "id": 41,
                        "description": "description 2",
                        "status": "BEING_TESTED",
                        "greetingMessage": "Hello! I am a cool agent! Give me a task!",
                        "agentTasks": [
                            {
                                "id": 1,
                                "description": "Some task",
                                "input": {
                                    "id": 1,
                                    "title": "Some title"
                                }
                            },
                            {
                                "id": 2,
                                "description": "Some task2",
                                "input": {
                                    "id": 2,
                                    "title": "Some title2"
                                }
                            }
                        ],
                        "agentSubscriptionPlans": [
                            {
                                "subscriptionInterval": "DAY",
                                "subscriptionIntervalCount": 1,
                                "capacity": 15,
                                "agentSubscriptionPlanPricings": [
                                    {
                                        "currency": "EUR",
                                        "salary": 5,
                                        "id": 41
                                    }
                                ],
                                "id": 41,
                                "agentSubscriptionPlanOwnerType": "USER"
                            },
                            {
                                "subscriptionInterval": "WEEK",
                                "subscriptionIntervalCount": 1,
                                "capacity": 15,
                                "agentSubscriptionPlanPricings": [
                                    {
                                        "currency": "EUR",
                                        "salary": 5,
                                        "id": 42
                                    }
                                ],
                                "id": 42,
                                "agentSubscriptionPlanOwnerType": "USER"
                            },
                            {
                                "subscriptionInterval": "MONTH",
                                "subscriptionIntervalCount": 1,
                                "capacity": 15,
                                "agentSubscriptionPlanPricings": [
                                    {
                                        "currency": "EUR",
                                        "salary": 5.04,
                                        "id": 43
                                    }
                                ],
                                "id": 43,
                                "agentSubscriptionPlanOwnerType": "USER"
                            },
                            {
                                "subscriptionInterval": "MONTH",
                                "subscriptionIntervalCount": 1,
                                "capacity": 15,
                                "agentSubscriptionPlanPricings": [
                                    {
                                        "currency": "EUR",
                                        "salary": 5.02,
                                        "id": 44
                                    }
                                ],
                                "id": 44,
                                "agentSubscriptionPlanOwnerType": "ORGANIZATION"
                            },
                            {
                                "subscriptionInterval": "YEAR",
                                "subscriptionIntervalCount": 1,
                                "capacity": 15,
                                "agentSubscriptionPlanPricings": [
                                    {
                                        "currency": "EUR",
                                        "salary": 5.04,
                                        "id": 45
                                    }
                                ],
                                "id": 45,
                                "agentSubscriptionPlanOwnerType": "ORGANIZATION"
                            }
                        ],
                        "agentsUser": {
                            "id": 1,
                            "firstName": "Aleksandr",
                            "lastName": "Nedorezov",
                            "email": "nedorezov@own.space"
                        },
                        "_links": [
                            {
                                "rel": "self",
                                "href": "/agentdata/41"
                            },
                            {
                                "rel": "agentsUser",
                                "href": "/users/1"
                            }
                        ]
                    },
                    {
                        "id": 21,
                        "description": "description 1",
                        "status": "BEING_TESTED",
                        "greetingMessage": "Hello! I am a super duper cool agent! Give me a task!",
                        "agentTasks": [
                            {
                                "id": 21,
                                "description": "Some task",
                                "input": {
                                    "id": 11,
                                    "title": "Some title"
                                }
                            },
                            {
                                "id": 22,
                                "description": "Some task2",
                                "input": {
                                    "id": 12,
                                    "title": "Some title2"
                                }
                            }
                        ],
                        "agentSubscriptionPlans": [
                            {
                                "subscriptionInterval": "DAY",
                                "subscriptionIntervalCount": 1,
                                "capacity": 15,
                                "agentSubscriptionPlanPricings": [
                                    {
                                        "currency": "EUR",
                                        "salary": 5,
                                        "id": 21
                                    }
                                ],
                                "id": 21,
                                "agentSubscriptionPlanOwnerType": "USER"
                            },
                            {
                                "subscriptionInterval": "WEEK",
                                "subscriptionIntervalCount": 1,
                                "capacity": 15,
                                "agentSubscriptionPlanPricings": [
                                    {
                                        "currency": "EUR",
                                        "salary": 5,
                                        "id": 22
                                    }
                                ],
                                "id": 22,
                                "agentSubscriptionPlanOwnerType": "USER"
                            },
                            {
                                "subscriptionInterval": "MONTH",
                                "subscriptionIntervalCount": 1,
                                "capacity": 15,
                                "agentSubscriptionPlanPricings": [
                                    {
                                        "currency": "EUR",
                                        "salary": 5.04,
                                        "id": 23
                                    }
                                ],
                                "id": 23,
                                "agentSubscriptionPlanOwnerType": "USER"
                            },
                            {
                                "subscriptionInterval": "MONTH",
                                "subscriptionIntervalCount": 1,
                                "capacity": 15,
                                "agentSubscriptionPlanPricings": [
                                    {
                                        "currency": "EUR",
                                        "salary": 5.02,
                                        "id": 24
                                    }
                                ],
                                "id": 24,
                                "agentSubscriptionPlanOwnerType": "ORGANIZATION"
                            },
                            {
                                "subscriptionInterval": "YEAR",
                                "subscriptionIntervalCount": 1,
                                "capacity": 15,
                                "agentSubscriptionPlanPricings": [
                                    {
                                        "currency": "EUR",
                                        "salary": 5.04,
                                        "id": 25
                                    }
                                ],
                                "id": 25,
                                "agentSubscriptionPlanOwnerType": "ORGANIZATION"
                            }
                        ],
                        "agentsUser": {
                            "id": 21,
                            "firstName": "Test",
                            "lastName": "Agent",
                            "email": "test@test.own.space"
                        },
                        "_links": [
                            {
                                "rel": "self",
                                "href": "/agentdata/21"
                            },
                            {
                                "rel": "agentsUser",
                                "href": "/users/21"
                            }
                        ]
                    }
                ],
                "_links": [
                    {
                        "rel": "self",
                        "href": "/agentdata"
                    }
                ]
            }

## POST /agentdata

Each agent data should contain daily, weekly, and monthly subscription plans.
Other subscription durations are not supported at the moment.

Each subscription plan should contain a subscription plan pricing with `EUR` as currency.
Currencies other than `EUR` are not supported at the moment.

Capacity should be > 0. Salary should be >=0.

For free plans salary should be set to 0.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentData+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
    + Body

            {
                "agentData":{
                    "agentsUserId":1,
                    "description":"description 2",
                    "status":"BEING_TESTED",
                    "greetingMessage":"Hello! I am a cool agent! Give me a task!",
                    "agentSubscriptionPlans":[
                        {
                            "subscriptionInterval":"DAY",
                            "subscriptionIntervalCount":1,
                            "capacity":15,
                            "agentSubscriptionPlanOwnerType":"USER",
                            "agentSubscriptionPlanPricings":[
                                {
                                    "currency":"EUR",
                                    "salary":5
                                }
                            ]
                        },
                        {
                            "subscriptionInterval":"WEEK",
                            "subscriptionIntervalCount":1,
                            "capacity":15,
                            "agentSubscriptionPlanOwnerType":"USER",
                            "agentSubscriptionPlanPricings":[
                                {
                                    "currency":"EUR",
                                    "salary":5
                                }
                            ]
                        },
                        {
                            "subscriptionInterval":"MONTH",
                            "subscriptionIntervalCount":1,
                            "capacity":15,
                            "agentSubscriptionPlanOwnerType":"USER",
                            "agentSubscriptionPlanPricings":[
                                {
                                    "currency":"EUR",
                                    "salary":5.035
                                }
                            ]
                        },
                        {
                            "subscriptionInterval":"MONTH",
                            "subscriptionIntervalCount":1,
                            "capacity":15,
                            "agentSubscriptionPlanOwnerType":"ORGANIZATION",
                            "agentSubscriptionPlanPricings":[
                                {
                                    "currency":"EUR",
                                    "salary":5.015
                                }
                            ]
                        },
                        {
                            "subscriptionInterval":"YEAR",
                            "subscriptionIntervalCount":1,
                            "capacity":15,
                            "agentSubscriptionPlanOwnerType":"ORGANIZATION",
                            "agentSubscriptionPlanPricings":[
                                {
                                    "currency":"EUR",
                                    "salary":5.035
                                }
                            ]
                        }
                    ]
                }
            }
            
+ Response 200 (application/vnd.uberblik.agentData+json)

    + Body
    
            {
                "agentData": {
                    "id": 41,
                    "description": "description 2",
                    "status": "BEING_TESTED",
                    "greetingMessage": "Hello! I am a cool agent! Give me a task!",
                    "agentTasks": [],
                    "agentSubscriptionPlans": [
                        {
                            "subscriptionInterval": "DAY",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5,
                                    "id": 41
                                }
                            ],
                            "id": 41,
                            "agentSubscriptionPlanOwnerType": "USER"
                        },
                        {
                            "subscriptionInterval": "WEEK",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5,
                                    "id": 42
                                }
                            ],
                            "id": 42,
                            "agentSubscriptionPlanOwnerType": "USER"
                        },
                        {
                            "subscriptionInterval": "MONTH",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5.035,
                                    "id": 43
                                }
                            ],
                            "id": 43,
                            "agentSubscriptionPlanOwnerType": "USER"
                        },
                        {
                            "subscriptionInterval": "MONTH",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5.015,
                                    "id": 44
                                }
                            ],
                            "id": 44,
                            "agentSubscriptionPlanOwnerType": "ORGANIZATION"
                        },
                        {
                            "subscriptionInterval": "YEAR",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5.035,
                                    "id": 45
                                }
                            ],
                            "id": 45,
                            "agentSubscriptionPlanOwnerType": "ORGANIZATION"
                        }
                    ],
                    "agentsUser": {
                        "id": 1,
                        "firstName": "Aleksandr",
                        "lastName": "Nedorezov",
                        "email": "nedorezov@own.space"
                    },
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/agentdata/41"
                        },
                        {
                            "rel": "agentsUser",
                            "href": "/users/1"
                        }
                    ]
                }
            }

## GET /agentdata/{agentDataId}

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentData+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.agentData+json)

    + Body
    
            {
                "agentData": {
                    "id": 21,
                    "description": "description 1",
                    "status": "BEING_TESTED",
                    "greetingMessage": "Hello! I am a cool agent! Give me a task!",
                    "agentTasks": [
                        {
                            "id": 21,
                            "description": "Some task",
                            "input": {
                                "id": 11,
                                "title": "Some title"
                            }
                        },
                        {
                            "id": 22,
                            "description": "Some task2",
                            "input": {
                                "id": 12,
                                "title": "Some title2"
                            }
                        }
                    ],
                    "agentSubscriptionPlans": [
                        {
                            "subscriptionInterval": "YEAR",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5.04,
                                    "id": 25
                                }
                            ],
                            "id": 25,
                            "agentSubscriptionPlanOwnerType": "ORGANIZATION"
                        },
                        {
                            "subscriptionInterval": "MONTH",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5.02,
                                    "id": 24
                                }
                            ],
                            "id": 24,
                            "agentSubscriptionPlanOwnerType": "ORGANIZATION"
                        },
                        {
                            "subscriptionInterval": "MONTH",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5.04,
                                    "id": 23
                                }
                            ],
                            "id": 23,
                            "agentSubscriptionPlanOwnerType": "USER"
                        },
                        {
                            "subscriptionInterval": "WEEK",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5,
                                    "id": 22
                                }
                            ],
                            "id": 22,
                            "agentSubscriptionPlanOwnerType": "USER"
                        },
                        {
                            "subscriptionInterval": "DAY",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5,
                                    "id": 21
                                }
                            ],
                            "id": 21,
                            "agentSubscriptionPlanOwnerType": "USER"
                        }
                    ],
                    "agentsUser": {
                        "id": 21,
                        "firstName": "Test",
                        "lastName": "Agent",
                        "email": "test@test.own.space"
                    },
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/agentdata/21"
                        },
                        {
                            "rel": "agentsUser",
                            "href": "/users/21"
                        }
                    ]
                }
            }

## GET /user/{userId}/agentdata

If `userId` is an id of the user logged in in the system (whose access token is send in request), 
request returns agentsData in which agentsUserId=`userId`.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentData+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.agentData+json)

    + Body
    
            {
                "agentData": {
                    "id": 21,
                    "description": "description 1",
                    "status": "BEING_TESTED",
                    "greetingMessage": "Hello! I am a cool agent! Give me a task!",
                    "agentTasks": [
                        {
                            "id": 21,
                            "description": "Some task",
                            "input": {
                                "id": 11,
                                "title": "Some title"
                            }
                        },
                        {
                            "id": 22,
                            "description": "Some task2",
                            "input": {
                                "id": 12,
                                "title": "Some title2"
                            }
                        }
                    ],
                    "agentSubscriptionPlans": [
                        {
                            "subscriptionInterval": "YEAR",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5.04,
                                    "id": 25
                                }
                            ],
                            "id": 25,
                            "agentSubscriptionPlanOwnerType": "ORGANIZATION"
                        },
                        {
                            "subscriptionInterval": "MONTH",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5.02,
                                    "id": 24
                                }
                            ],
                            "id": 24,
                            "agentSubscriptionPlanOwnerType": "ORGANIZATION"
                        },
                        {
                            "subscriptionInterval": "MONTH",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5.04,
                                    "id": 23
                                }
                            ],
                            "id": 23,
                            "agentSubscriptionPlanOwnerType": "USER"
                        },
                        {
                            "subscriptionInterval": "WEEK",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5,
                                    "id": 22
                                }
                            ],
                            "id": 22,
                            "agentSubscriptionPlanOwnerType": "USER"
                        },
                        {
                            "subscriptionInterval": "DAY",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5,
                                    "id": 21
                                }
                            ],
                            "id": 21,
                            "agentSubscriptionPlanOwnerType": "USER"
                        }
                    ],
                    "agentsUser": {
                        "id": 21,
                        "firstName": "Test",
                        "lastName": "Agent",
                        "email": "test@test.own.space"
                    },
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/agentdata/21"
                        },
                        {
                            "rel": "agentsUser",
                            "href": "/users/21"
                        }
                    ]
                }
            }

## PUT /agentdata/{agentDataId}

JSON with any of the fields given in requests body (not necessary all of them), will also be a valid body for this request. Therefore, in the request body, you may only pass those user parameters, which you want to modify.


`agentSubscriptionPlans` can be `null` or empty.

`capacity` field for an agent subscription plan is not obligatory.

`agentSubscriptionPlanPricings` can be `null` or empty.

`salary` field for an agent subscription plan pricing is not obligatory.


It is possible to pass only those agent subscription plans that should be edited.
It is not obligatory to pass all of the agents subscription plans.


As, at the moment, all of the agents should have daily, weekly, and monthly subscription plans,
and only them, it is not possible to modify `subscriptionInterval`, 
and `subscriptionIntervalCount` values, since it is not necessary.

As, at the moment, all subscription plans should have `EUR` as currency, and only it,
it is not possible to change the currency of subscription plan pricing.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentData+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
    + Body
    
            {
                "agentData": {
                    "agentsUserId": 21,
                    "description": "description 212",
                    "status": "BEING_TESTED",
                    "greetingMessage": "Hi! I am a cool agent! Give me a task!",
                    "agentSubscriptionPlans": [
                        {
                            "agentSubscriptionPlanPricings": [
                                {
                                    "salary": 2.02,
                                    "id": 24
                                }
                            ],
                            "id": 24
                        },
                        {
                            "capacity": 115,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "salary": 1.04,
                                    "id": 25
                                }
                            ],
                            "id": 25
                        }
                    ]
                }
            }
            
+ Response 200 (application/vnd.uberblik.agentData+json)

    + Body
    
            {
                "agentData": {
                    "id": 21,
                    "description": "description 212",
                    "status": "BEING_TESTED",
                    "greetingMessage": "Hi! I am a cool agent! Give me a task!",
                    "agentTasks": [],
                    "agentSubscriptionPlans": [
                        {
                            "subscriptionInterval": "YEAR",
                            "subscriptionIntervalCount": 1,
                            "capacity": 115,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 1.04,
                                    "id": 25
                                }
                            ],
                            "id": 25,
                            "agentSubscriptionPlanOwnerType": "ORGANIZATION"
                        },
                        {
                            "subscriptionInterval": "MONTH",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 2.02,
                                    "id": 24
                                }
                            ],
                            "id": 24,
                            "agentSubscriptionPlanOwnerType": "ORGANIZATION"
                        },
                        {
                            "subscriptionInterval": "MONTH",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5.04,
                                    "id": 23
                                }
                            ],
                            "id": 23,
                            "agentSubscriptionPlanOwnerType": "USER"
                        },
                        {
                            "subscriptionInterval": "WEEK",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5,
                                    "id": 22
                                }
                            ],
                            "id": 22,
                            "agentSubscriptionPlanOwnerType": "USER"
                        },
                        {
                            "subscriptionInterval": "DAY",
                            "subscriptionIntervalCount": 1,
                            "capacity": 15,
                            "agentSubscriptionPlanPricings": [
                                {
                                    "currency": "EUR",
                                    "salary": 5,
                                    "id": 21
                                }
                            ],
                            "id": 21,
                            "agentSubscriptionPlanOwnerType": "USER"
                        }
                    ],
                    "agentsUser": {
                        "id": 21,
                        "firstName": "Test",
                        "lastName": "Agent",
                        "email": "test@test.own.space"
                    },
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/agentdata/21"
                        },
                        {
                            "rel": "agentsUser",
                            "href": "/users/21"
                        }
                    ]
                }
            }

## DELETE /agentdata/{agentDataId}

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentData+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200

# Group Agent Tasks

Entity AgentTask stores the description of the task to be performed by the agent, 
id of agentData entity (reference to which agent that task belongs), 
and an id of input entity (which is a form for agents configuration).

Note that as agent_task_id is stored in each element, we can reffer which agentTask is assigned to the element, if any.

## GET /agentdata/{agentDataId}/agenttasks

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentTask+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.agentsTasks+json)

    + Body
    
            {
                "agentTasks": [
                    {
                        "id": 21,
                        "description": "Search for news by super duper awesome picture analysis.",
                        "input": {
                            "id": 22,
                            "title": "News Agent input form 4-2."
                        },
                        "_links": [
                            {
                                "rel": "self",
                                "href": "/agentdata/2/agenttasks/21"
                            },
                            {
                                "rel": "input",
                                "href": "/inputs/22"
                            }
                        ]
                    },
                    {
                        "id": 3,
                        "description": "Search for news by keyword",
                        "input": {
                            "id": 3,
                            "title": "News Agent input form 3. Ururu"
                        },
                        "_links": [
                            {
                                "rel": "self",
                                "href": "/agentdata/2/agenttasks/3"
                            },
                            {
                                "rel": "input",
                                "href": "/inputs/3"
                            }
                        ]
                    }
                ],
                "_links": [
                    {
                        "rel": "self",
                        "href": "/agentdata/2/agenttasks"
                    }
                ]
            }

## POST /agentdata/{agentDataId}/agenttasks

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentTask+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
    + Body
    
            {
              "agentTask": {
                "description": "Search for news by picture recognition. What? Why Not?!",
                "inputId": 21
              }
            }
            
+ Response 200 (application/vnd.uberblik.agentTask+json)

    + Body
    
            {
                "agentTask": {
                    "id": 21,
                    "description": "Search for news by picture recognition. What? Why Not?!",
                    "input": {
                        "id": 21,
                        "title": "News Agent input form #4. For picture recognition and some other stuff."
                    },
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/agentdata/2/agenttasks/21"
                        },
                        {
                            "rel": "agentData",
                            "href": "/agentdata/2"
                        },
                        {
                            "rel": "input",
                            "href": "/inputs/21"
                        }
                    ]
                }
            }

## GET /agentdata/{agentDataId}/agenttasks/{agentTaskId}

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentTask+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.agentTask+json)

    + Body
    
            {
                "agentTask": {
                    "id": 21,
                    "description": "Search for news by picture recognition. What? Why Not?!",
                    "input": {
                        "id": 21,
                        "title": "News Agent input form #4. For picture recognition and some other stuff."
                    },
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/agentdata/2/agenttasks/21"
                        },
                        {
                            "rel": "agentData",
                            "href": "/agentdata/2"
                        },
                        {
                            "rel": "input",
                            "href": "/inputs/21"
                        }
                    ]
                }
            }

## PUT /agentdata/{agentDataId}/agenttasks/{agentTaskId}

JSON with any of the fields given in requests body (not necessary all of them), will also be a valid body for this request. Therefore, in the request body, you may only pass those user parameters, which you want to modify.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentTask+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
    + Body
    
            {
              "agentTask": {
                "description": "Search for news by super duper awesome picture analysis.",
                "inputId": 22
              }
            }
            
+ Response 200 (application/vnd.uberblik.agentTask+json)

    + Body
    
            {
                "agentTask": {
                    "id": 21,
                    "description": "Search for news by super duper awesome picture analysis.",
                    "input": {
                        "id": 22,
                        "title": "By which picture you want me to search news?"
                    },
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/agentdata/2/agenttasks/21"
                        },
                        {
                            "rel": "agentData",
                            "href": "/agentdata/2"
                        },
                        {
                            "rel": "input",
                            "href": "/inputs/22"
                        }
                    ]
                }
            }

## DELETE /agentdata/{agentDataId}/agenttasks/{agentTaskId}

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentTask+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200

# Group Agent Task Configurations

Those requests are "shortcuts" which can be used to set-up or get 
all the entities necessary for agent tasks configuration.

It is also possible to set-up/get all of the data described here 
via separate requests corresponding to particular entities.
Though it will require to sent more requests.

**NOTE:** responses describes in this section don't contain links to entities (yet?).
In each response each entity contains its id from the server, which can be used in requests. 

**NOTE:** Possible questionType values are: `SINGLE_CHOICE`, `MULTIPLE_CHOICE`, and `DROPDOWN`.

**NOTE:** `isGolden` field in `questionAnswer` is designed to store the correctness of an answer, 
when forms will be used to store questionnaires.

## POST /agentdata/{agentDataId}/agenttasks/configuration

This request creates an agent task for agentData with id=`agentDataId`, 
and defines a configuration form for that agentTask.

**NOTE:** At the moment `isGolden` field is not mandatory in the requests to configure agentTasks.
However, it is recommended to pass it with the `true` value for answers that should be selected by default,
since later on it may be decided to have agent tasks pre-configured.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentTaskConfiguration+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
    + Body
    
            {
                "agentTask":{
                    "description":"description 21",
                    "input":{
                        "title":"Some title",
                        "indexedInputFields":[
                            {
                                "index":1,
                                "inputElement":{
                                    "question":{
                                        "text":"Huh?",
                                        "questionType":"SINGLE_CHOICE",
                                        "questionAnswers":[
                                            {
                                                "answer":"Huh indeed",
                                                "isGolden":true
                                            },
                                            {
                                                "answer":"Carrot",
                                                "isGolden":false
                                            },
                                            {
                                                "answer":"potato",
                                                "isGolden":false
                                            },
                                            {
                                                "answer":"rabbit",
                                                "isGolden":false
                                            }
                                        ]
                                    }
                                }
                            },
                            {
                                "index":2,
                                "inputElement":{
                                    "question":{
                                        "text":"To what 2+2 equals to?",
                                        "questionType":"MULTIPLE_CHOICE",
                                        "questionAnswers":[
                                            {
                                                "answer":"4",
                                                "isGolden":true
                                            },
                                            {
                                                "answer":"3",
                                                "isGolden":false
                                            },
                                            {
                                                "answer":"45",
                                                "isGolden":false
                                            },
                                            {
                                                "answer":"1+3",
                                                "isGolden":true
                                            }
                                        ]
                                    }
                                }
                            },
                            {
                                "index":1,
                                "inputElement":{
                                    "question":{
                                        "text":"How many carrots are in your fridge?",
                                        "questionType":"DROPDOWN",
                                        "questionAnswers":[
                                            {
                                                "answer":"1 Carrot",
                                                "isGolden":false
                                            },
                                            {
                                                "answer":"2 Carrots",
                                                "isGolden":false
                                            },
                                            {
                                                "answer":"3 Carrots",
                                                "isGolden":false
                                            },
                                            {
                                                "answer":"More carrots then just 3",
                                                "isGolden":true
                                            }
                                        ]
                                    }
                                }
                            },
                            {
                                "index":4,
                                "inputElement":{
                                    "textbox":{
                                        "placeholder":"this is a demo placeholder 1111111111111",
                                        "goldenText":"this is a text to be compared to",
                                        "isMultiline":true
                                    }
                                }
                            },
                            {
                                "index":5,
                                "inputElement":{
                                    "textbox":{
                                        "placeholder":"this is a demo placeholder 222222",
                                        "goldenText":"this is a text to be compared to 2",
                                        "isMultiline":false
                                    }
                                }
                            }
                        ]
                    }
                }
            }
            
+ Response 200 (application/vnd.uberblik.agentTaskConfiguration+json)

    + Body
    
            {
                "agentTask":{
                    "description":"description 21",
                    "input":{
                        "title":"Some title",
                        "indexedInputFields":[
                            {
                                "index":1,
                                "inputElementType":"QUESTION",
                                "id":421,
                                "inputElement":{
                                    "question":{
                                        "text":"Huh?",
                                        "questionType":"SINGLE_CHOICE",
                                        "questionAnswers":[
                                            {
                                                "answer":"Huh indeed",
                                                "isGolden":true,
                                                "id":441
                                            },
                                            {
                                                "answer":"Carrot",
                                                "isGolden":false,
                                                "id":442
                                            },
                                            {
                                                "answer":"potato",
                                                "isGolden":false,
                                                "id":443
                                            },
                                            {
                                                "answer":"rabbit",
                                                "isGolden":false,
                                                "id":444
                                            }
                                        ],
                                        "id":381
                                    }
                                },
                                "inputElementAnswers":[
                                    {
                                        "agentTaskQuestionAnswers":[
            
                                        ]
                                    }
                                ]
                            },
                            {
                                "index":2,
                                "inputElementType":"QUESTION",
                                "id":422,
                                "inputElement":{
                                    "question":{
                                        "text":"To what 2+2 equals to?",
                                        "questionType":"MULTIPLE_CHOICE",
                                        "questionAnswers":[
                                            {
                                                "answer":"4",
                                                "isGolden":true,
                                                "id":445
                                            },
                                            {
                                                "answer":"3",
                                                "isGolden":false,
                                                "id":446
                                            },
                                            {
                                                "answer":"45",
                                                "isGolden":false,
                                                "id":447
                                            },
                                            {
                                                "answer":"1+3",
                                                "isGolden":true,
                                                "id":448
                                            }
                                        ],
                                        "id":382
                                    }
                                },
                                "inputElementAnswers":[
                                    {
                                        "agentTaskQuestionAnswers":[
            
                                        ]
                                    }
                                ]
                            },
                            {
                                "index":1,
                                "inputElementType":"QUESTION",
                                "id":423,
                                "inputElement":{
                                    "question":{
                                        "text":"How many carrots are in your fridge?",
                                        "questionType":"DROPDOWN",
                                        "questionAnswers":[
                                            {
                                                "answer":"1 Carrot",
                                                "isGolden":false,
                                                "id":449
                                            },
                                            {
                                                "answer":"2 Carrots",
                                                "isGolden":false,
                                                "id":450
                                            },
                                            {
                                                "answer":"3 Carrots",
                                                "isGolden":false,
                                                "id":451
                                            },
                                            {
                                                "answer":"More carrots then just 3",
                                                "isGolden":true,
                                                "id":452
                                            }
                                        ],
                                        "id":383
                                    }
                                },
                                "inputElementAnswers":[
                                    {
                                        "agentTaskQuestionAnswers":[
            
                                        ]
                                    }
                                ]
                            },
                            {
                                "index":4,
                                "inputElementType":"TEXTBOX",
                                "id":424,
                                "inputElement":{
                                    "textbox":{
                                        "id":361,
                                        "placeholder":"this is a demo placeholder 1111111111111",
                                        "goldenText":"this is a text to be compared to",
                                        "isMultiline":true
                                    }
                                },
                                "inputElementAnswers":[
                                    {
                                        "agentTaskTextboxAnswer":null
                                    }
                                ]
                            },
                            {
                                "index":5,
                                "inputElementType":"TEXTBOX",
                                "id":425,
                                "inputElement":{
                                    "textbox":{
                                        "id":362,
                                        "placeholder":"this is a demo placeholder 222222",
                                        "goldenText":"this is a text to be compared to 2",
                                        "isMultiline":false
                                    }
                                },
                                "inputElementAnswers":[
                                    {
                                        "agentTaskTextboxAnswer":null
                                    }
                                ]
                            }
                        ],
                        "id":441
                    },
                    "id":261,
                    "agentData":{
                        "id":61,
                        "agentsUserId":1,
                        "description":"description 1",
                        "salary":100.99,
                        "capacity":100,
                        "status":"BEING_TESTED"
                    }
                }
            }

## PUT /agentdata/{agentDataId}/agenttasks/{agentTaskId}/configuration

This request modified an agent task with id=`agentTaskId`, and defines modified configuration form for that agentTask.

**NOTE:** At the moment `isGolden` field is not mandatory in the requests to configure agentTasks.
However, it is recommended to pass it with the `true` value for answers that should be selected by default,
since later on it may be decided to have agent tasks pre-configured.

**NOTE:** If any of existing indexed input fields are excluded from request (their ids are not stated in the request),
 they will be deleted from the form.

Similarly, if any of existing question answers are excluded from request (their ids are not stated in the request), 
they will be deleted from the form.

It is crucial that `index`es are set for each and every one of `indexedInputField`s.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentTaskConfiguration+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
    + Body
    
            {
                "agentTask":{
                    "description":"Some task",
                    "input":{
                        "title":"Some title",
                        "indexedInputFields":[
                            {
                                "index":1,
                                "inputElementType":"QUESTION",
                                "id":66,
                                "inputElement":{
                                    "question":{
                                        "text":"Huh?",
                                        "questionType":"SINGLE_CHOICE",
                                        "questionAnswers":[
                                            {
                                                "id":133,
                                                "answer":"Huh indeed",
                                                "isGolden":true
                                            },
                                            {
                                                "id":134,
                                                "answer":"Carrot",
                                                "isGolden":false
                                            },
                                            {
                                                "id":135,
                                                "answer":"potato",
                                                "isGolden":false
                                            },
                                            {
                                                "answer":"ha",
                                                "isGolden":false
                                            }
                                        ],
                                        "id":64
                                    }
                                }
                            },
                            {
                                "index":2,
                                "inputElementType":"QUESTION",
                                "id":67,
                                "inputElement":{
                                    "question":{
                                        "text":"To what 2+2 equals to?",
                                        "questionType":"MULTIPLE_CHOICE",
                                        "questionAnswers":[
                                            {
                                                "id":137,
                                                "answer":"4",
                                                "isGolden":true
                                            },
                                            {
                                                "id":139,
                                                "answer":"45",
                                                "isGolden":false
                                            },
                                            {
                                                "id":140,
                                                "answer":"1+3",
                                                "isGolden":true
                                            },
                                            {
                                                "answer":"1+2+1",
                                                "isGolden":true
                                            }
                                        ],
                                        "id":65
                                    }
                                }
                            },
                            {
                                "index":3,
                                "inputElementType":"QUESTION",
                                "id":68,
                                "inputElement":{
                                    "question":{
                                        "text":"How many carrots are in your fridge?",
                                        "questionType":"DROPDOWN",
                                        "questionAnswers":[
                                            {
                                                "id":141,
                                                "answer":"1 Carrot",
                                                "isGolden":false
                                            },
                                            {
                                                "id":142,
                                                "answer":"2 Carrots",
                                                "isGolden":false
                                            },
                                            {
                                                "id":143,
                                                "answer":"3 Carrots",
                                                "isGolden":false
                                            },
                                            {
                                                "id":144,
                                                "answer":"More carrots then just 3",
                                                "isGolden":true
                                            }
                                        ],
                                        "id":66
                                    }
                                }
                            },
                            {
                                "index":4,
                                "inputElementType":"TEXTBOX",
                                "id":69,
                                "inputElement":{
                                    "textbox":{
                                        "id":63,
                                        "label":"label1",
                                        "placeholder":"this is a demo placeholder 1111111111111",
                                        "goldenText":"this is a text to be compared to",
                                        "isMultiline":true
                                    }
                                }
                            },
                            {
                                "index":5,
                                "inputElementType":"TEXTBOX",
                                "id":70,
                                "inputElement":{
                                    "textbox":{
                                        "id":64,
                                        "label":"label2",
                                        "placeholder":"this is a demo placeholder 222222",
                                        "goldenText":"this is a text to be compared to 2",
                                        "isMultiline":false
                                    }
                                }
                            },
                            {
                                "index":6,
                                "inputElementType":"TEXTBOX",
                                "inputElement":{
                                    "textbox":{
                                        "label":"label3",
                                        "placeholder":"this is a demo placeholder 3",
                                        "goldenText":"this is a text to be compared to 3",
                                        "isMultiline":false
                                    }
                                }
                            }
                        ],
                        "id":62
                    }
                }
            }
            
+ Response 200 (application/vnd.uberblik.agentTaskConfiguration+json)

    + Body
    
            {
                "agentTask":{
                    "description":"Some task",
                    "input":{
                        "title":"Some title",
                        "indexedInputFields":[
                            {
                                "index":1,
                                "inputElementType":"QUESTION",
                                "id":66,
                                "inputElement":{
                                    "question":{
                                        "text":"Huh?",
                                        "questionType":"SINGLE_CHOICE",
                                        "questionAnswers":[
                                            {
                                                "id":133,
                                                "answer":"Huh indeed",
                                                "isGolden":true
                                            },
                                            {
                                                "id":134,
                                                "answer":"Carrot",
                                                "isGolden":false
                                            },
                                            {
                                                "id":135,
                                                "answer":"potato",
                                                "isGolden":false
                                            },
                                            {
                                                "id":165,
                                                "answer":"ha",
                                                "isGolden":false
                                            }
                                        ],
                                        "id":64
                                    }
                                },
                                "inputElementAnswers":[
                                    {
                                        "agentTaskQuestionAnswers":[
            
                                        ]
                                    }
                                ]
                            },
                            {
                                "index":2,
                                "inputElementType":"QUESTION",
                                "id":67,
                                "inputElement":{
                                    "question":{
                                        "text":"To what 2+2 equals to?",
                                        "questionType":"MULTIPLE_CHOICE",
                                        "questionAnswers":[
                                            {
                                                "id":137,
                                                "answer":"4",
                                                "isGolden":true
                                            },
                                            {
                                                "id":139,
                                                "answer":"45",
                                                "isGolden":false
                                            },
                                            {
                                                "id":140,
                                                "answer":"1+3",
                                                "isGolden":true
                                            },
                                            {
                                                "id":166,
                                                "answer":"1+2+1",
                                                "isGolden":true
                                            }
                                        ],
                                        "id":65
                                    }
                                },
                                "inputElementAnswers":[
                                    {
                                        "agentTaskQuestionAnswers":[
            
                                        ]
                                    }
                                ]
                            },
                            {
                                "index":3,
                                "inputElementType":"QUESTION",
                                "id":68,
                                "inputElement":{
                                    "question":{
                                        "text":"How many carrots are in your fridge?",
                                        "questionType":"DROPDOWN",
                                        "questionAnswers":[
                                            {
                                                "id":141,
                                                "answer":"1 Carrot",
                                                "isGolden":false
                                            },
                                            {
                                                "id":142,
                                                "answer":"2 Carrots",
                                                "isGolden":false
                                            },
                                            {
                                                "id":143,
                                                "answer":"3 Carrots",
                                                "isGolden":false
                                            },
                                            {
                                                "id":144,
                                                "answer":"More carrots then just 3",
                                                "isGolden":true
                                            }
                                        ],
                                        "id":66
                                    }
                                },
                                "inputElementAnswers":[
                                    {
                                        "agentTaskQuestionAnswers":[
            
                                        ]
                                    }
                                ]
                            },
                            {
                                "index":4,
                                "inputElementType":"TEXTBOX",
                                "id":69,
                                "inputElement":{
                                    "textbox":{
                                        "id":63,
                                        "label":"label1",
                                        "placeholder":"this is a demo placeholder 1111111111111",
                                        "goldenText":"this is a text to be compared to",
                                        "isMultiline":true
                                    }
                                },
                                "inputElementAnswers":[
                                    {
                                        "agentTaskTextboxAnswer":null
                                    }
                                ]
                            },
                            {
                                "index":5,
                                "inputElementType":"TEXTBOX",
                                "id":70,
                                "inputElement":{
                                    "textbox":{
                                        "id":64,
                                        "label":"label2",
                                        "placeholder":"this is a demo placeholder 222222",
                                        "goldenText":"this is a text to be compared to 2",
                                        "isMultiline":false
                                    }
                                },
                                "inputElementAnswers":[
                                    {
                                        "agentTaskTextboxAnswer":null
                                    }
                                ]
                            },
                            {
                                "index":5,
                                "inputElementType":"TEXTBOX",
                                "id":103,
                                "inputElement":{
                                    "textbox":{
                                        "id":83,
                                        "label":"label3",
                                        "placeholder":"this is a demo placeholder 3",
                                        "goldenText":"this is a text to be compared to 3",
                                        "isMultiline":false
                                    }
                                },
                                "inputElementAnswers":[
                                    {
                                        "agentTaskTextboxAnswer":null
                                    }
                                ]
                            }
                        ],
                        "id":62
                    },
                    "id":62,
                    "agentData":{
                        "agentsUserId":1,
                        "description":"description 2",
                        "status":"BEING_TESTED",
                        "id":1
                    }
                }
            }

## GET /agentdata/{agentDataId}/agenttasks/{agentTaskId}/configuration

This request returns configuration for agent task with id=`agentTaskId`.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentTaskConfiguration+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.agentTaskConfiguration+json)

    + Body
    
            {
                "agentTask":{
                    "description":"description 21",
                    "input":{
                        "title":"Some title",
                        "indexedInputFields":[
                            {
                                "index":1,
                                "inputElementType":"QUESTION",
                                "id":21,
                                "inputElement":{
                                    "question":{
                                        "text":"demo text",
                                        "questionType":"SINGLE_CHOICE",
                                        "questionAnswers":[
                                            {
                                                "answer":"Carrot - yep",
                                                "isGolden":true,
                                                "id":42
                                            },
                                            {
                                                "answer":"Carrot 2",
                                                "isGolden":false,
                                                "id":43
                                            },
                                            {
                                                "answer":"Carrot 2",
                                                "isGolden":false,
                                                "id":44
                                            },
                                            {
                                                "answer":"Carrot",
                                                "isGolden":false,
                                                "id":45
                                            }
                                        ],
                                        "id":41
                                    }
                                },
                                "inputElementAnswers":[
                                    {
                                        "agentTaskQuestionAnswers":[
                                            {
                                                "id":21,
                                                "questionAnswer":{
                                                    "id":42,
                                                    "answer":"Carrot - yep",
                                                    "isGolden":true
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "index":2,
                                "inputElementType":"QUESTION",
                                "id":22,
                                "inputElement":{
                                    "question":{
                                        "text":"demo text",
                                        "questionType":"MULTIPLE_CHOICE",
                                        "questionAnswers":[
                                            {
                                                "answer":"Carrot - yep",
                                                "isGolden":true,
                                                "id":46
                                            },
                                            {
                                                "answer":"Carrot 2",
                                                "isGolden":false,
                                                "id":47
                                            },
                                            {
                                                "answer":"Carrot 3 - yep",
                                                "isGolden":true,
                                                "id":48
                                            },
                                            {
                                                "answer":"Carrot",
                                                "isGolden":false,
                                                "id":49
                                            }
                                        ],
                                        "id":42
                                    }
                                },
                                "inputElementAnswers":[
                                    {
                                        "agentTaskQuestionAnswers":[
                                            {
                                                "id":23,
                                                "questionAnswer":{
                                                    "id":48,
                                                    "answer":"Carrot 3 - yep",
                                                    "isGolden":true
                                                }
                                            },
                                            {
                                                "id":22,
                                                "questionAnswer":{
                                                    "id":46,
                                                    "answer":"Carrot - yep",
                                                    "isGolden":true
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "index":3,
                                "inputElementType":"QUESTION",
                                "id":23,
                                "inputElement":{
                                    "question":{
                                        "text":"demo text",
                                        "questionType":"DROPDOWN",
                                        "questionAnswers":[
                                            {
                                                "answer":"I am a potato!",
                                                "isGolden":false,
                                                "id":50
                                            },
                                            {
                                                "answer":"awdawddwa 2",
                                                "isGolden":false,
                                                "id":51
                                            },
                                            {
                                                "answer":"Carrot 3 - yep",
                                                "isGolden":true,
                                                "id":52
                                            },
                                            {
                                                "answer":"Carrot",
                                                "isGolden":false,
                                                "id":53
                                            }
                                        ],
                                        "id":43
                                    }
                                },
                                "inputElementAnswers":[
                                    {
                                        "agentTaskQuestionAnswers":[
                                            {
                                                "id":24,
                                                "questionAnswer":{
                                                    "id":52,
                                                    "answer":"Carrot 3 - yep",
                                                    "isGolden":true
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "index":4,
                                "inputElementType":"TEXTBOX",
                                "id":24,
                                "inputElement":{
                                    "textbox":{
                                        "id":21,
                                        "placeholder":"this is a demo placeholder 1111111111111",
                                        "goldenText":"this is a text to be compared to",
                                        "isMultiline":true
                                    }
                                },
                                "inputElementAnswers":[
                                    {
                                        "agentTaskTextboxAnswer":{
                                            "id":21,
                                            "answer":"this is a demo answer 111"
                                        }
                                    }
                                ]
                            },
                            {
                                "index":5,
                                "inputElementType":"TEXTBOX",
                                "id":25,
                                "inputElement":{
                                    "textbox":{
                                        "id":22,
                                        "placeholder":"this is a demo placeholder for a one-line textbox",
                                        "goldenText":"this is a text to be compared to",
                                        "isMultiline":false
                                    }
                                },
                                "inputElementAnswers":[
                                    {
                                        "agentTaskTextboxAnswer":{
                                            "id":22,
                                            "answer":"this is a demo answer 1112222"
                                        }
                                    }
                                ]
                            }
                        ],
                        "id":41
                    },
                    "id":41,
                    "agentData":{
                        "id":2,
                        "agentsUserId":22,
                        "description":"Check for news on the given topic.",
                        "salary":10,
                        "capacity":1,
                        "status":"ACTIVE"
                    }
                }
            }

# Group Agent Task Elements

This section describes requests for assignment of agent tasks to elements.

## POST /agentdata/{agentDataId}/agenttasks/{agentTaskId}/boards/{boardId}/elements/{elementId}/agenttaskelements

+ Request
    + Headers
    
            Accept: application/vnd.uberblik.agentTaskElement+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4         
            
+ Response 200 (application/vnd.uberblik.agentTaskElement+json)

    + Body
    
            {
                "agentTaskElement":{
                    "agentTaskId":161,
                    "elementId":101,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/agentdata/61/agenttasks/161/boards/1/elements/101/agenttaskelements"
                        },
                        {
                            "rel":"agentTask",
                            "href":"/agentdata/61/agenttasks/161"
                        },
                        {
                            "rel":"element",
                            "href":"/boards/1/elements/101"
                        }
                    ]
                }
            }

## GET /agentdata/{agentDataId}/agenttasks/{agentTaskId}/boards/{boardId}/elements/{elementId}/agenttaskelements

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentTaskElement+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.agentTaskElement+json)

    + Body
    
            {
                "agentTaskElement":{
                    "agentTaskId":161,
                    "elementId":101,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/agentdata/61/agenttasks/161/boards/1/elements/101/agenttaskelements"
                        },
                        {
                            "rel":"agentTask",
                            "href":"/agentdata/61/agenttasks/161"
                        },
                        {
                            "rel":"element",
                            "href":"/boards/1/elements/101"
                        }
                    ]
                }
            }

+ Response 404

## DELETE /agentdata/{agentDataId}/agenttasks/{agentTaskId}/boards/{boardId}/elements/{elementId}/agenttaskelements

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentTaskElement+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200

# Group Agent Task Element Answers

This section describes requests for saving answers to agent tasks assigned to specific elements.

## POST /agentdata/{agentDataId}/agenttasks/{agentTaskId}/boards/{boardId}/elements/{elementId}/answers

This request deletes previusly stored answers for an agent task for with id=`agentTaskId`, 
and saves new answers, specified in the requests body.

Request can be freely used by users with emails ending with `@own.space`, 
`@agent.own.space`, and `@test.own.space`.
Other users should have an active subscription for the agent with id=`agentDataId` 
with number of performed queries < capacity.

Returns (for users that don't have own.space email):

`402001 PAYMENT_REQUIRED` No paid task queries available. 
User who made a request has used all tasks he/she paid for the agent with id=`agentDataId`, 
or his/her subscription is expired.

`402002 PAYMENT_REQUIRED` Subscription of user who made a request to an agent with id=`agentDataId` is expired.

`402003 PAYMENT_REQUIRED` Subscription of user who made a request to an agent with id=`agentDataId` is expired 
and we were not able to charge for renewal with provided payment method.

`402004 PAYMENT_REQUIRED` No paid task queries available. 
User who made a request has used all tasks he/she paid for the agent with id=`agentDataId`.

`503001 SERVICE_UNAVAILABLE` Subscription of user who made a request to an agent with id=`agentDataId` is expired. 
Cannot retrieve a subscription from Stripe to validate it was renewed.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentTaskElement+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
    + Body
    
            {
                "agentTask":{
                    "input":{
                        "id":341,
                        "indexedInputFields":[
                            {
                                "id":321,
                                "inputElementAnswers":[
                                    {
                                        "agentTaskQuestionAnswers":[
                                            {
                                                "questionAnswer":{
                                                    "id":322
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "id":322,
                                "inputElementAnswers":[
                                    {
                                        "agentTaskQuestionAnswers":[
                                            {
                                                "questionAnswer":{
                                                    "id":327
                                                }
                                            },
                                            {
                                                "questionAnswer":{
                                                    "id":326
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "id":323,
                                "inputElementAnswers":[
                                    {
                                        "agentTaskQuestionAnswers":[
                                            {
                                                "questionAnswer":{
                                                    "id":329
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "id":324,
                                "inputElementAnswers":[
                                    {
                                        "agentTaskTextboxAnswer":{
                                            "answer":"new looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong answer, as it is multiline"
                                        }
                                    }
                                ]
                            },
                            {
                                "id":325,
                                "inputElementAnswers":[
                                    {
                                        "agentTaskTextboxAnswer":{
                                            "answer":"new shorter answer"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
            
+ Response 200 (application/vnd.uberblik.agentTaskElement+json)

    + Body
    
            {
                "agentTaskElement":{
                    "agentTask":{
                        "description":"description 21",
                        "input":{
                            "title":"Some title",
                            "indexedInputFields":[
                                {
                                    "index":1,
                                    "inputElementType":"QUESTION",
                                    "id":321,
                                    "inputElement":{
                                        "question":{
                                            "text":"demo text",
                                            "questionType":"SINGLE_CHOICE",
                                            "questionAnswers":[
                                                {
                                                    "answer":"Carrot - yep",
                                                    "isGolden":true,
                                                    "id":321
                                                },
                                                {
                                                    "answer":"Carrot 2",
                                                    "isGolden":false,
                                                    "id":322
                                                },
                                                {
                                                    "answer":"Carrot 2",
                                                    "isGolden":false,
                                                    "id":323
                                                },
                                                {
                                                    "answer":"Carrot",
                                                    "isGolden":false,
                                                    "id":324
                                                }
                                            ],
                                            "id":281
                                        }
                                    },
                                    "inputElementAnswers":[
                                        {
                                            "agentTaskQuestionAnswers":[
                                                {
                                                    "id":1,
                                                    "questionAnswer":{
                                                        "id":322,
                                                        "answer":"Carrot 2",
                                                        "isGolden":false
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "index":2,
                                    "inputElementType":"QUESTION",
                                    "id":322,
                                    "inputElement":{
                                        "question":{
                                            "text":"demo text",
                                            "questionType":"MULTIPLE_CHOICE",
                                            "questionAnswers":[
                                                {
                                                    "answer":"Carrot - yep",
                                                    "isGolden":true,
                                                    "id":325
                                                },
                                                {
                                                    "answer":"Carrot 2",
                                                    "isGolden":false,
                                                    "id":326
                                                },
                                                {
                                                    "answer":"Carrot 3 - yep",
                                                    "isGolden":true,
                                                    "id":327
                                                },
                                                {
                                                    "answer":"Carrot",
                                                    "isGolden":false,
                                                    "id":328
                                                }
                                            ],
                                            "id":282
                                        }
                                    },
                                    "inputElementAnswers":[
                                        {
                                            "agentTaskQuestionAnswers":[
                                                {
                                                    "id":3,
                                                    "questionAnswer":{
                                                        "id":326,
                                                        "answer":"Carrot 2",
                                                        "isGolden":false
                                                    }
                                                },
                                                {
                                                    "id":2,
                                                    "questionAnswer":{
                                                        "id":327,
                                                        "answer":"Carrot 3 - yep",
                                                        "isGolden":true
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "index":3,
                                    "inputElementType":"QUESTION",
                                    "id":323,
                                    "inputElement":{
                                        "question":{
                                            "text":"demo text",
                                            "questionType":"DROPDOWN",
                                            "questionAnswers":[
                                                {
                                                    "answer":"I am a potato!",
                                                    "isGolden":false,
                                                    "id":329
                                                },
                                                {
                                                    "answer":"awdawddwa 2",
                                                    "isGolden":false,
                                                    "id":330
                                                },
                                                {
                                                    "answer":"Carrot 3 - yep",
                                                    "isGolden":true,
                                                    "id":331
                                                },
                                                {
                                                    "answer":"Carrot",
                                                    "isGolden":false,
                                                    "id":332
                                                }
                                            ],
                                            "id":283
                                        }
                                    },
                                    "inputElementAnswers":[
                                        {
                                            "agentTaskQuestionAnswers":[
                                                {
                                                    "id":4,
                                                    "questionAnswer":{
                                                        "id":329,
                                                        "answer":"I am a potato!",
                                                        "isGolden":false
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "index":4,
                                    "inputElementType":"TEXTBOX",
                                    "id":324,
                                    "inputElement":{
                                        "textbox":{
                                            "id":261,
                                            "label":"default label",
                                            "placeholder":"this is a demo placeholder 1111111111111",
                                            "goldenText":"this is a text to be compared to",
                                            "isMultiline":true
                                        }
                                    },
                                    "inputElementAnswers":[
                                        {
                                            "agentTaskTextboxAnswer":{
                                                "id":1,
                                                "answer":"new looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong answer, as it is multiline"
                                            }
                                        }
                                    ]
                                },
                                {
                                    "index":5,
                                    "inputElementType":"TEXTBOX",
                                    "id":325,
                                    "inputElement":{
                                        "textbox":{
                                            "id":262,
                                            "label":"default label",
                                            "placeholder":"this is a demo placeholder for a one-line textbox",
                                            "goldenText":"this is a text to be compared to",
                                            "isMultiline":false
                                        }
                                    },
                                    "inputElementAnswers":[
                                        {
                                            "agentTaskTextboxAnswer":{
                                                "id":2,
                                                "answer":"new shorter answer"
                                            }
                                        }
                                    ]
                                }
                            ],
                            "id":341
                        },
                        "id":161,
                        "agentData":{
                            "id":61,
                            "agentsUserId":1,
                            "description":"description 1",
                            "salary":100.99,
                            "capacity":100,
                            "status":"BEING_TESTED"
                        }
                    },
                    "elementId":101
                }
            }

## GET /agentdata/{agentDataId}/agenttasks/{agentTaskId}/boards/{boardId}/elements/{elementId}/answers

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.agentTaskElement+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.agentTaskElement+json)

    + Body
    
            {
                "agentTaskElement":{
                    "agentTask":{
                        "description":"description 21",
                        "input":{
                            "title":"Some title",
                            "indexedInputFields":[
                                {
                                    "index":1,
                                    "inputElementType":"QUESTION",
                                    "id":321,
                                    "inputElement":{
                                        "question":{
                                            "text":"demo text",
                                            "questionType":"SINGLE_CHOICE",
                                            "questionAnswers":[
                                                {
                                                    "answer":"Carrot - yep",
                                                    "isGolden":true,
                                                    "id":321
                                                },
                                                {
                                                    "answer":"Carrot 2",
                                                    "isGolden":false,
                                                    "id":322
                                                },
                                                {
                                                    "answer":"Carrot 2",
                                                    "isGolden":false,
                                                    "id":323
                                                },
                                                {
                                                    "answer":"Carrot",
                                                    "isGolden":false,
                                                    "id":324
                                                }
                                            ],
                                            "id":281
                                        }
                                    },
                                    "inputElementAnswers":[
                                        {
                                            "agentTaskQuestionAnswers":[
                                                {
                                                    "id":1,
                                                    "questionAnswer":{
                                                        "id":322,
                                                        "answer":"Carrot 2",
                                                        "isGolden":false
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "index":2,
                                    "inputElementType":"QUESTION",
                                    "id":322,
                                    "inputElement":{
                                        "question":{
                                            "text":"demo text",
                                            "questionType":"MULTIPLE_CHOICE",
                                            "questionAnswers":[
                                                {
                                                    "answer":"Carrot - yep",
                                                    "isGolden":true,
                                                    "id":325
                                                },
                                                {
                                                    "answer":"Carrot 2",
                                                    "isGolden":false,
                                                    "id":326
                                                },
                                                {
                                                    "answer":"Carrot 3 - yep",
                                                    "isGolden":true,
                                                    "id":327
                                                },
                                                {
                                                    "answer":"Carrot",
                                                    "isGolden":false,
                                                    "id":328
                                                }
                                            ],
                                            "id":282
                                        }
                                    },
                                    "inputElementAnswers":[
                                        {
                                            "agentTaskQuestionAnswers":[
                                                {
                                                    "id":3,
                                                    "questionAnswer":{
                                                        "id":326,
                                                        "answer":"Carrot 2",
                                                        "isGolden":false
                                                    }
                                                },
                                                {
                                                    "id":2,
                                                    "questionAnswer":{
                                                        "id":327,
                                                        "answer":"Carrot 3 - yep",
                                                        "isGolden":true
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "index":3,
                                    "inputElementType":"QUESTION",
                                    "id":323,
                                    "inputElement":{
                                        "question":{
                                            "text":"demo text",
                                            "questionType":"DROPDOWN",
                                            "questionAnswers":[
                                                {
                                                    "answer":"I am a potato!",
                                                    "isGolden":false,
                                                    "id":329
                                                },
                                                {
                                                    "answer":"awdawddwa 2",
                                                    "isGolden":false,
                                                    "id":330
                                                },
                                                {
                                                    "answer":"Carrot 3 - yep",
                                                    "isGolden":true,
                                                    "id":331
                                                },
                                                {
                                                    "answer":"Carrot",
                                                    "isGolden":false,
                                                    "id":332
                                                }
                                            ],
                                            "id":283
                                        }
                                    },
                                    "inputElementAnswers":[
                                        {
                                            "agentTaskQuestionAnswers":[
                                                {
                                                    "id":4,
                                                    "questionAnswer":{
                                                        "id":329,
                                                        "answer":"I am a potato!",
                                                        "isGolden":false
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "index":4,
                                    "inputElementType":"TEXTBOX",
                                    "id":324,
                                    "inputElement":{
                                        "textbox":{
                                            "id":261,
                                            "label":"default label",
                                            "placeholder":"this is a demo placeholder 1111111111111",
                                            "goldenText":"this is a text to be compared to",
                                            "isMultiline":true
                                        }
                                    },
                                    "inputElementAnswers":[
                                        {
                                            "agentTaskTextboxAnswer":{
                                                "id":1,
                                                "answer":"new looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong answer, as it is multiline"
                                            }
                                        }
                                    ]
                                },
                                {
                                    "index":5,
                                    "inputElementType":"TEXTBOX",
                                    "id":325,
                                    "inputElement":{
                                        "textbox":{
                                            "id":262,
                                            "label":"default label",
                                            "placeholder":"this is a demo placeholder for a one-line textbox",
                                            "goldenText":"this is a text to be compared to",
                                            "isMultiline":false
                                        }
                                    },
                                    "inputElementAnswers":[
                                        {
                                            "agentTaskTextboxAnswer":{
                                                "id":2,
                                                "answer":"new shorter answer"
                                            }
                                        }
                                    ]
                                }
                            ],
                            "id":341
                        },
                        "id":161,
                        "agentData":{
                            "id":61,
                            "agentsUserId":1,
                            "description":"description 1",
                            "salary":100.99,
                            "capacity":100,
                            "status":"BEING_TESTED"
                        }
                    },
                    "elementId":101
                }
            }

+ Response 404

# Group User Agent Subscriptions

This section describes requests for users subscriptions to agents.

## POST /agentdata/{agentDataId}/agentsubscriptionplans/{agentSubscriptionPlanId}/agentsubscriptionplanpricings/{agentSubscriptionPlanPricingId}/useragentsubscriptions

The request will return `403 BAD REQUEST` response if user sending the request
is already subscribed to an agent with id `agentDataId`.

Returns:
`200` if subscription was created successfully

`403 FORBIDDEN` if user who made a request is already subscribed to an agent with id=`agentDataId`

`400 BAD_REQUEST` if neither first name nor last name is filled

`403 FOBIDDEN` Stripe payment method source should be not null for non-free subscriptions.

`503 SERVICE_UNAVAILABLE` Error during user-agent subscription via stripe. 
Cannot create a subscription in Stripe.

`503 SERVICE_UNAVAILABLE` Error during user-agent subscription via stripe. 
Cannot update customers default payment method source in Stripe for user who made a request.

`503 SERVICE_UNAVAILABLE` Error during user-agent subscription via stripe. Cannot create a customer in Stripe.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.userAgentSubscription+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
    + Body
    
            {
              "userAgentSubscription": {
                "stripePaymentMethodSource": "src_18eYalADawdaZp1l9ZTjSU0",
                "stripeClientSecret": "scs_such_secret_so_wow",
                "firstName": "Aleksandr",
                "lastName": "Nedorezov",
                "companyName": "OOO OWN"
              }
            }
            
+ Response 200 (application/vnd.uberblik.userAgentSubscription+json)

    + Body
    
            {
                "userAgentSubscription":{
                    "id":1,
                    "groklandUserId":1,
                    "userEmail":"nedorezov@own.space",
                    "agentData":{
                        "agentsUserId":21,
                        "description":"description 2",
                        "status":"INACTIVE",
                        "id":501
                    },
                    "agentSubscriptionPlanPricing":{
                        "currency":"EUR",
                        "salary":5.0,
                        "id":282
                    },
                    "expirationDate":1530186732858,
                    "capacity":15,
                    "performedQueries":0,
                    "renewAfterExpiration":true,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/useragentsubscriptions/1"
                        },
                        {
                            "rel":"groklandUser",
                            "href":"/users/1"
                        }
                    ]
                }
            }
            
## POST /agentdata/{agentDataId}/useragentsubscriptions/unsubscribe

The request will return `404 NOT FOUND` response if user sending the request
is not subscribed to an agent with id `agentDataId`.

Returns:
`200` if subscription was created successfully

`503 SERVICE_UNAVAILABLE` Error during user-agent subscription cancellation in stripe. 
Cannot get a subscription from Stripe or/and cancel it.

`404 NOT_FOUND` User who made a request is not subscribed to an agent with id=`agentDataId`

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.userAgentSubscription+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.userAgentSubscription+json)

    + Body
    
            {
                "userAgentSubscription":{
                    "id":1,
                    "groklandUserId":1,
                    "userEmail":"nedorezov@own.space",
                    "agentData":{
                        "agentsUserId":21,
                        "description":"description 2",
                        "status":"INACTIVE",
                        "id":501
                    },
                    "agentSubscriptionPlanPricing":{
                        "currency":"EUR",
                        "salary":5.0,
                        "id":282
                    },
                    "expirationDate":1530186732858,
                    "capacity":15,
                    "performedQueries":0,
                    "renewAfterExpiration":false,
                    "_links":[
                        {
                            "rel":"self",
                            "href":"/useragentsubscriptions/1"
                        },
                        {
                            "rel":"groklandUser",
                            "href":"/users/1"
                        }
                    ]
                }
            }
            
+ Response 403

## GET /useragentsubscriptions?status=active

Returns users active subscriptions.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.userAgentSubscription+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.userAgentSubscription+json)

    + Body
    
            {
                "userAgentSubscriptions":[
                    {
                        "id":81,
                        "groklandUserId":1,
                        "userEmail":"nedorezov@own.space",
                        "agentData":{
                            "agentsUserId":2,
                            "description":"description 2",
                            "status":"INACTIVE",
                            "id":61
                        },
                        "agentSubscriptionPlanPricing":{
                            "currency":"EUR",
                            "salary":5.01,
                            "id":41
                        },
                        "expirationDate":1530625608078,
                        "capacity":15,
                        "performedQueries":0,
                        "renewAfterExpiration":false,
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/useragentsubscriptions/81"
                            },
                            {
                                "rel":"groklandUser",
                                "href":"/users/1"
                            }
                        ]
                    }
                ],
                "_links":[
                    {
                        "rel":"self",
                        "href":"/useragentsubscriptions"
                    }
                ]
            }

+ Response 404

## GET /useragentsubscriptions

Returns all users subscriptions, including expired, and cancelled.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.userAgentSubscription+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.userAgentSubscription+json)

    + Body
    
            {
                "userAgentSubscriptions":[
                    {
                        "id":21,
                        "groklandUserId":1,
                        "userEmail":"nedorezov@own.space",
                        "agentData":{
                            "agentsUserId":21,
                            "description":"description 2",
                            "status":"INACTIVE",
                            "id":501
                        },
                        "agentSubscriptionPlanPricing":{
                            "currency":"EUR",
                            "salary":5.0,
                            "id":282
                        },
                        "expirationDate":1530187074532,
                        "capacity":15,
                        "performedQueries":2,
                        "renewAfterExpiration":true,
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/useragentsubscriptions/21"
                            },
                            {
                                "rel":"groklandUser",
                                "href":"/users/1"
                            }
                        ]
                    },
                    {
                        "id":1,
                        "groklandUserId":1,
                        "userEmail":"nedorezov@own.space",
                        "agentData":{
                            "agentsUserId":21,
                            "description":"description 2",
                            "status":"INACTIVE",
                            "id":501
                        },
                        "agentSubscriptionPlanPricing":{
                            "currency":"EUR",
                            "salary":5.0,
                            "id":282
                        },
                        "expirationDate":1530186732858,
                        "capacity":15,
                        "performedQueries":15,
                        "renewAfterExpiration":false,
                        "_links":[
                            {
                                "rel":"self",
                                "href":"/useragentsubscriptions/1"
                            },
                            {
                                "rel":"groklandUser",
                                "href":"/users/1"
                            }
                        ]
                    }
                ],
                "_links":[
                    {
                        "rel":"self",
                        "href":"/useragentsubscriptions"
                    }
                ]
            }

+ Response 404

## GET /useragentsubscriptions/{userAgentSubscriptionId}

Returns userAgentSubscription with id=`userAgentSubscriptionId` if it exists,
and it belongs to the user requesting it.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.userAgentSubscription+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.userAgentSubscription+json)

    + Body
    
            {
                "userAgentSubscription": {
                    "id": 181,
                    "groklandUserId": 1,
                    "userEmail": "nedorezov@own.space",
                    "agentData": {
                        "agentsUserId": 2,
                        "description": "description 2",
                        "status": "INACTIVE",
                        "id": 61
                    },
                    "agentSubscriptionPlanPricing": {
                        "currency": "EUR",
                        "salary": 5.01,
                        "id": 41
                    },
                    "expirationDate": 1530965992691,
                    "capacity": 15,
                    "performedQueries": 0,
                    "renewAfterExpiration": true,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/useragentsubscriptions/181"
                        },
                        {
                            "rel": "groklandUser",
                            "href": "/users/1"
                        }
                    ]
                }
            }

+ Response 404

# Group User Stripe Customer

As user subscribes to an agent, his/her payment details are securely stored at Stripe.
It is possible to retrieve this data, to that form with payment details will be pre-filled 
on users consecutive payments with data he/she entered before.

## GET /users/{userId}/userstripecustomers?currency={Currency}

At the moment only `EUR` is a currency we support.

If `Currency` parameter will contain data different from one of supported currencies,
`403 BAD REQUEST` response will be returned.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.userStripeCustomer+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.userStripeCustomer+json)

    + Body
    
            {
                "userStripeCustomer": {
                    "groklandUserId": 1,
                    "currency": "EUR",
                    "stripePaymentMethodSource": "src_18eYalAHEMiOZZp1l9ZTjSU0",
                    "stripeClientSecret": "secret_uu_key",
                    "firstName": "Aleksandr",
                    "lastName": "Nedorezov",
                    "companyName": "OOO OWN",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/users/1/userstripecustomers/21"
                        },
                        {
                            "rel": "groklandUser",
                            "href": "/users/1"
                        }
                    ]
                }
            }
            
+ Response 403
            
## GET /users/{userId}/userstripecustomers/{userStripeCustomerId}

If userStripeCustomer entity with id=`userStripeCustomerId` is not related to a user with id=`userId`,
`403 BAD REQUEST` response will be returned.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.userStripeCustomer+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.userStripeCustomer+json)

    + Body
    
            {
                "userStripeCustomer": {
                    "groklandUserId": 1,
                    "currency": "EUR",
                    "stripePaymentMethodSource": "src_18eYalAHEMiOZZp1l9ZTjSU0",
                    "stripeClientSecret": "secret_uu_key",
                    "firstName": "Aleksandr",
                    "lastName": "Nedorezov",
                    "companyName": "OOO OWN",
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/users/1/userstripecustomers/21"
                        },
                        {
                            "rel": "groklandUser",
                            "href": "/users/1"
                        }
                    ]
                }
            }

# Group Organization Agent Subscriptions

This section describes requests for organizations subscriptions to agents.

Possible agent subscription product types are `AGENT` and `AGENT_PACKAGE`.

`agentSubscriptionProductId` represents an id of an entity specified in `agentSubscriptionProductType` field.

## POST /organizationsubscriptions/organizations/{organizationId}/agentdata/{agentDataId}/subscriptionplans/{agentSubscriptionPlanId}

Returns:
`200` if subscription was created successfully

`403 FORBIDDEN` if an organization to be subscribed is already subscribed to an agent with id=`agentDataId`

`400 BAD_REQUEST` if neither first name nor last name is filled

`403 FOBIDDEN` Stripe payment method source should be not null for non-free subscriptions.

`503 SERVICE_UNAVAILABLE` Error during organization-agent subscription via stripe. 
Cannot create a subscription in Stripe.

`503 SERVICE_UNAVAILABLE` Error during organization-agent subscription via stripe. 
Cannot update customers default payment method source in Stripe for user who made a request.

`503 SERVICE_UNAVAILABLE` Error during organization-agent subscription via stripe. Cannot create a customer in Stripe.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.organizationAgentSubscription+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
    + Body
    
            {
                "organizationAgentSubscription": {
                    "stripePaymentMethodSource": "src_RaNdOmSymBols",
                    "firstName": "Aleksandr",
                    "lastName": "Nedorezov",
                    "companyName": "OOO OWN",
                    "currency": "EUR"
                }
            }
            
+ Response 200 (application/vnd.uberblik.organizationAgentSubscription+json)

    + Body
    
            {
                "organizationAgentSubscription": {
                    "id": 101,
                    "organizationId": 1,
                    "organizationName": "A Cool Organization",
                    "agentSubscriptionProductId": 1,
                    "agentSubscriptionProductType": "AGENT",
                    "expirationDate": 1573897206049,
                    "capacity": 15,
                    "performedQueries": 0,
                    "agentSubscriptionPlanPricing": {
                        "currency": "EUR",
                        "salary": 5.04,
                        "id": 5
                    },
                    "renewAfterExpiration": true,
                    "planMultiplier": 1,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/organizationsubscriptions/organizations/1/agents/subscription/101"
                        },
                        {
                            "rel": "organizationAgentSubscription",
                            "href": "/organizations/1"
                        }
                    ]
                }
            }
            
## PATCH /organizationsubscriptions/organizations/{organizationId}/agentdata/{agentDataId}

Returns:
`200` if subscription auto-renewal was cancelled successfully

`503 SERVICE_UNAVAILABLE` Error during organization-agent subscription cancellation in stripe. 
Cannot get a subscription from Stripe or/and cancel it.

`404 NOT_FOUND` Organization to be unsubscribed is not subscribed to an agent with id=`agentDataId`

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.organizationAgentSubscription+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.organizationAgentSubscription+json)

    + Body
    
            {
                "organizationAgentSubscription": {
                    "id": 101,
                    "organizationId": 1,
                    "organizationName": "A Cool Organization",
                    "agentSubscriptionProductId": 1,
                    "agentSubscriptionProductType": "AGENT",
                    "expirationDate": 1573897206049,
                    "capacity": 15,
                    "performedQueries": 0,
                    "agentSubscriptionPlanPricing": {
                        "currency": "EUR",
                        "salary": 5.04,
                        "id": 5
                    },
                    "renewAfterExpiration": false,
                    "planMultiplier": 1,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/organizationsubscriptions/organizations/1/agents/subscription/101"
                        },
                        {
                            "rel": "organizationAgentSubscription",
                            "href": "/organizations/1"
                        }
                    ]
                }
            }
            
+ Response 403

## GET /organizationsubscriptions/organizations/{organizationId}?status=active

Returns organizations active subscriptions.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.organizationSubscriptions+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.organizationSubscriptions+json)

    + Body

            {
                "organizationSubscriptions": {
                    "organizationAgentSubscriptions": [
                        {
                            "id": 101,
                            "organizationId": 1,
                            "organizationName": "A Cool Organization",
                            "agentSubscriptionProductId": 1,
                            "agentSubscriptionProductType": "AGENT",
                            "expirationDate": 1573897206049,
                            "capacity": 15,
                            "performedQueries": 0,
                            "agentSubscriptionPlanPricing": {
                                "currency": "EUR",
                                "salary": 5.04,
                                "id": 5
                            },
                            "renewAfterExpiration": true,
                            "planMultiplier": 1,
                            "_links": [
                                {
                                    "rel": "self",
                                    "href": "/organizationsubscriptions/organizations/1/agents/subscription/101"
                                },
                                {
                                    "rel": "organizationAgentSubscription",
                                    "href": "/organizations/1"
                                }
                            ]
                        }
                    ],
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/organizationsubscriptions/organizations/1"
                        }
                    ]
                }
            }

+ Response 404

## GET /organizationsubscriptions/organizations/{organizationId}

Returns all organizations subscriptions, including expired, and cancelled.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.organizationAgentSubscription+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.organizationAgentSubscription+json)

    + Body
    
            {
                "organizationSubscriptions": {
                    "organizationAgentSubscriptions": [
                        {
                            "id": 1,
                            "organizationId": 1,
                            "organizationName": "OOO OWN",
                            "agentSubscriptionProductId": 1,
                            "agentSubscriptionProductType": "AGENT",
                            "expirationDate": 1573744465769,
                            "capacity": 15,
                            "performedQueries": 0,
                            "agentSubscriptionPlanPricing": {
                                "currency": "EUR",
                                "salary": 5.04,
                                "id": 5
                            },
                            "renewAfterExpiration": false,
                            "planMultiplier": 1,
                            "_links": [
                                {
                                    "rel": "self",
                                    "href": "/organizationsubscriptions/organizations/1/agents/subscription/1"
                                },
                                {
                                    "rel": "organizationAgentSubscription",
                                    "href": "/organizations/1"
                                }
                            ]
                        },
                        {
                            "id": 101,
                            "organizationId": 1,
                            "organizationName": "A Cool Organization",
                            "agentSubscriptionProductId": 1,
                            "agentSubscriptionProductType": "AGENT",
                            "expirationDate": 1573897206049,
                            "capacity": 15,
                            "performedQueries": 0,
                            "agentSubscriptionPlanPricing": {
                                "currency": "EUR",
                                "salary": 5.04,
                                "id": 5
                            },
                            "renewAfterExpiration": true,
                            "planMultiplier": 1,
                            "_links": [
                                {
                                    "rel": "self",
                                    "href": "/organizationsubscriptions/organizations/1/agents/subscription/101"
                                },
                                {
                                    "rel": "organizationAgentSubscription",
                                    "href": "/organizations/1"
                                }
                            ]
                        }
                    ],
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/organizationsubscriptions/organizations/1"
                        }
                    ]
                }
            }

+ Response 404

## GET /organizationsubscriptions/organizations/{organizationId}/agents/subscription/{organizationAgentSubscriptionId}

Returns organizationAgentSubscription with id=`organizationAgentSubscriptionId` if it exists,
and it belongs to the organization in which user requesting the subscription is a member.

+ Request

    + Headers
    
            Accept: application/vnd.uberblik.organizationAgentSubscription+json;charset:UTF-8
            access-token : uywg87gw6gf6g468gf46g4f6g34f4f4
            
+ Response 200 (application/vnd.uberblik.organizationAgentSubscription+json)

    + Body
    
            {
                "organizationAgentSubscription": {
                    "id": 61,
                    "organizationId": 1,
                    "organizationName": "A Cool Organization",
                    "agentSubscriptionProductId": 1,
                    "agentSubscriptionProductType": "AGENT",
                    "expirationDate": 1573803735944,
                    "capacity": 15,
                    "performedQueries": 0,
                    "agentSubscriptionPlanPricing": {
                        "currency": "EUR",
                        "salary": 5.04,
                        "id": 5
                    },
                    "renewAfterExpiration": false,
                    "planMultiplier": 1,
                    "_links": [
                        {
                            "rel": "self",
                            "href": "/organizationsubscriptions/organizations/1/agents/subscription/61"
                        },
                        {
                            "rel": "organizationAgentSubscription",
                            "href": "/organizations/1"
                        }
                    ]
                }
            }

+ Response 404
