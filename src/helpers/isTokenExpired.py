from datetime import datetime as dt, timedelta

def isTokenExpired(token):
  tokenCreatedAt = dt.strptime(token, '%Y-%m-%d %H:%M:%S.%f')
  nextWeekCreationDate = tokenCreatedAt + timedelta(days=7)
  
  todayDatetime = dt.now()

  isTokenExpired = todayDatetime > nextWeekCreationDate

  print(isTokenExpired)

  return isTokenExpired