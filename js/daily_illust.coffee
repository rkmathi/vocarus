$ ->
  StartDate = new Date(2012, 9, 5)
  diff = parseInt((new Date().getTime() / 1000 - StartDate.getTime() / 1000) / (60 * 60 * 24))
  index_today = diff % 4
  day_str = ['miku', 'gumi', 'mikustand', 'luka']
  $('.miku').append('<div class="' + day_str[index_today] + '_image"><img src="images/' + day_str[index_today] + '.png" alt="day_str[index_today]"></div>')
  return
