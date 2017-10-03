import requests
import webbrowser


def get_folder(id):
    '''
    get item list of folder
    :param id: the id of folder
    :return: item list
    '''
    url = "https://clients6.google.com/drive/v2internal/files"
    params = {
        "appDataFilter": "NO_APP_DATA",
        "corpora": "default",
        "errorRecovery": "false",
        "fields": "kind,nextPageToken,items(kind,title,mimeType,createdDate,modifiedDate,modifiedByMeDate,lastViewedByMeDate,fileSize,owners(kind,permissionId,displayName,picture,emailAddress,domain),lastModifyingUser(kind,permissionId,displayName,picture,emailAddress),hasThumbnail,thumbnailVersion,iconLink,id,shared,sharedWithMeDate,userPermission(role),explicitlyTrashed,quotaBytesUsed,shareable,copyable,subscribed,folderColor,hasChildFolders,fileExtension,primarySyncParentId,sharingUser(kind,permissionId,displayName,picture,emailAddress),flaggedForAbuse,folderFeatures,spaces,sourceAppId,editable,recency,recencyReason,version,actionItems,teamDriveId,hasAugmentedPermissions,primaryDomainName,organizationDisplayName,passivelySubscribed,trashingUser(kind,permissionId,displayName,picture,emailAddress),trashedDate,hasVisitorPermissions,parents(id),labels(starred,hidden,trashed,restricted,viewed),capabilities(canCopy,canDownload,canEdit,canAddChildren,canDelete,canRemoveChildren,canShare,canTrash,canRename,canReadTeamDrive,canMoveTeamDriveItem,canMoveItemIntoTeamDrive)),incompleteSearch",
        "includeTeamDriveItems": "true",
        "key": "AIzaSyAy9VVXHSpS2IJpptzYtGbLP3-3_l0aBk4",
        "maxResults": "50",
        "openDrive": "false",
        "orderBy": "folder,modifiedDate desc",
        "q": "trashed = false and '%s' in parents" % id,
        "reason": "102",
        "spaces": "drive,photos",
        "supportsTeamDrives": "true",
        "syncType": "0",
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.8",
        "authorization": "SAPISIDHASH 1507167332_29f29e7e1831df2b2d2a61e61b1fb108c62961ea_e",
        "cookie": "SID=PwVvE7ClsXFAHW28npv5kb_7ZE63fKJi_UeJuTphLW3M19GSShbxryb9XB6F3BtksRp99w.; HSID=A7aMu9DSfNtYDcUlW; SSID=Av1e7NvshSietHGLx; APISID=KfJRU9o8h2f-rt0I/AR-mzz4w0XMJInPeT; SAPISID=bJHPszHYk5Ssa5Zq/AiJUzODqVvYmXpniv; NID=113=ZOqp6cBH27bOLoVEHUBAlzNE5OGyIeQl6akrD_AotqY59LTiKiYi-E8j3T0ZUaAeBVsXRJX6RxSH6SsMDGCSQ7D4sNh1f3fjAqcqrUThVlTFhueKAA8cCMmTfVf7ENPMWTknVAu4HcoDukTQphJixuIJ3eVaiuNB6luo6ae_45LjCpx82eo; 1P_JAR=2017-10-5-1; SIDCC=AE4kn7_PPFb5VIMVJ0Tfi8YeipmO4Oj0A_9hgya0nAQWqcrzq1GzFZs5mz90oR5m6TqOz6gNU61bytdTg0M",
        "origin": "https://drive.google.com",
        "referer": "https://drive.google.com/drive/folders/0B414hrAL3fTJbVB5MG9PS1U2ek0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "x-goog-authuser": "0",
        "Host": "clients6.google.com"
    }
    resp = requests.get(url, headers=headers, params=params, verify=False)
    items = resp.json()["items"]
    return items


def downloadfile(id):
    '''
    download the file
    :param id: the file id
    :param filepath: the local file path
    :return:
    '''
    url = "https://drive.google.com/uc?id=%s&export=download" % id
    webbrowser.open(url, new=0, autoraise=True)


if __name__ == "__main__":
    # items = get_folder("0B2p1zXqO0zzpOTBldmxoUjhrQlk")
    # for item in items:
    #     print(item["title"], item["id"])
    
    downloadfile("0B6h7SF4LjjaUZ1VrYW5tbWd0RlE")
