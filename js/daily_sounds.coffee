$ ->
  StartDate = new Date(2012, 9, 5)
  diff = parseInt((new Date().getTime() / 1000 - StartDate.getTime() / 1000) / (60 * 60 * 24))
  index_today = if diff % 4 isnt 2 then diff % 4 else 0
  day_str = ['miku', 'gumi', '_miku', 'luka']
  singer_name =
    'miku': '初音ミク'
    'gumi': 'GUMI'
    '_miku': '_初音ミク'
    'luka': '巡音ルカ'

  songs_name = [
    ["夕焼け小焼け", "シャボン玉"]
    ["きらきら星", "どんぐりころころ","さくら"]
    ["_"]
    ["あめふり", "ひなまつり", "ロンドン橋落ちた", "荒城の月"]
  ]

  status = ['before', 'after']
  for i in [0..2]
    $('</p>').append("音源: VOCALOID&trade;2 #{singer_name[day_str[index_today]]}").prependTo(".service_demo:eq(#{i})")
    $('</p>').append("曲名: #{songs_name[index_today][i]}").prependTo(".service_demo:eq(#{i})")
    for j in [0..1]
      $('.service_text').eq(i*2+j).after("<audio class='service_audio' controls><source src='audio/#{day_str[index_today]}#{i}_#{status[j]}.ogg' type='audio/ogg'><source src='audio/#{day_str[index_today]}#{i}_#{status[j]}.mp3' type='audio/mpeg'></audio>")

  return
