#!/usr/bin/env python3
"""注入更新后的字库数据到HTML，并更新JS逻辑"""
import re

# 1. 读取chardb_full.js中的数据块
with open('C:/Users/Administrator/WorkBuddy/2026-06-02-task-5/chardb_full.js', 'r', encoding='utf-8') as f:
    db_content = f.read()

# 提取 CHAR_DB_FULL 数组内容
db_start = db_content.find('const CHAR_DB_FULL = [')
db_end = db_content.rfind('];')
db_block = db_content[db_start:db_end+2]
# 重命名为 CHAR_DB_RAW
db_block = db_block.replace('const CHAR_DB_FULL = [', 'const CHAR_DB_RAW = [')

# 2. 读取HTML文件
with open('C:/Users/Administrator/WorkBuddy/2026-06-02-task-5/识字训练应用.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 3. 替换字库数据块
old_db_start = html.find('const CHAR_DB_RAW = [')
old_state_start = html.find('// ====================== 状态管理 ======================')
html = html[:old_db_start] + db_block + '\n\n' + html[old_state_start:]

# 4. 更新 CHARS 映射 (增加 radical 和 strokeCount)
old_chars_map = """const CHARS = CHAR_DB_RAW.map((row,idx)=>({
  id: idx,
  char: row[0],
  pinyin: row[1],
  meaning: row[2],
  grade: parseInt(row[3]),
  reading: row[4]
}));"""

new_chars_map = """const CHARS = CHAR_DB_RAW.map((row,idx)=>({
  id: idx,
  char: row[0],
  pinyin: row[1],
  meaning: row[2],
  grade: parseInt(row[3]),
  reading: row[4],
  radical: row[5] || '?',
  strokeCount: parseInt(row[6]) || 0
}));"""

html = html.replace(old_chars_map, new_chars_map)

# 5. 更新数据格式注释
html = html.replace(
    '// 精选500字核心字库（含完整数据），其余以结构存储\n// 每字格式：[字, 拼音, 释义, 年级, 专属小阅读]\n// 小学1-6年级国标3000常用字完整数据库\n// 格式：[汉字, 拼音, 释义, 年级, 专属小阅读]',
    '// 精选500字核心字库（含完整数据），其余以结构存储\n// 每字格式：[字, 拼音, 释义, 年级, 专属小阅读, 偏旁部首, 笔画数]\n// 小学1-6年级国标3000常用字完整数据库\n// 格式：[汉字, 拼音, 释义, 年级, 专属小阅读, 偏旁部首, 笔画数]'
)

# 6. 更新题型选择区 - 增加部首和笔画题型
old_quiz_types = """      <div class="filter-row">
        <label>题型：</label>
        <div class="grade-btns">
          <button class="grade-btn active" data-qt="char2py" onclick="setQuizType(this,'char2py')">字→拼音</button>
          <button class="grade-btn" data-qt="py2char" onclick="setQuizType(this,'py2char')">拼音→字</button>
          <button class="grade-btn" data-qt="char2meaning" onclick="setQuizType(this,'char2meaning')">字→释义</button>
        </div>
      </div>"""

new_quiz_types = """      <div class="filter-row">
        <label>题型：</label>
        <div class="grade-btns">
          <button class="grade-btn active" data-qt="char2py" onclick="setQuizType(this,'char2py')">字→拼音</button>
          <button class="grade-btn" data-qt="py2char" onclick="setQuizType(this,'py2char')">拼音→字</button>
          <button class="grade-btn" data-qt="char2meaning" onclick="setQuizType(this,'char2meaning')">字→释义</button>
          <button class="grade-btn" data-qt="char2radical" onclick="setQuizType(this,'char2radical')">字→部首</button>
          <button class="grade-btn" data-qt="char2stroke" onclick="setQuizType(this,'char2stroke')">字→笔画数</button>
        </div>
      </div>"""

html = html.replace(old_quiz_types, new_quiz_types)

# 7. 更新 showQuizQuestion 函数 - 增加部首和笔画题型
old_show_quiz = """function showQuizQuestion(target,pool){
  let wrongOpts=shuffle(pool.filter(c=>c.char!==target.char)).slice(0,3);
  let opts=shuffle([target,...wrongOpts]);
  const area=document.getElementById('quiz-area');

  let question='',optHtml='';
  if(currentQuizType==='char2py'){
    question=`<div class="quiz-char">${target.char}</div><div style="text-align:center;color:#888;font-size:13px;margin-bottom:4px">这个字的读音是？</div>`;
    optHtml=opts.map(o=>`<button class="quiz-opt" onclick="checkAnswer(this,'${target.char}','${o.char}','${target.pinyin}','${o.pinyin}')">${o.pinyin}</button>`).join('');
  }else if(currentQuizType==='py2char'){
    question=`<div class="quiz-char" style="font-size:40px;padding:20px 0">${target.pinyin}</div><div style="text-align:center;color:#888;font-size:13px;margin-bottom:4px">这个读音对应哪个汉字？</div>`;
    optHtml=opts.map(o=>`<button class="quiz-opt" onclick="checkAnswer(this,'${target.char}','${o.char}','${target.char}','${o.char}')">${o.char}</button>`).join('');
  }else{
    question=`<div class="quiz-char">${target.char}</div><div style="text-align:center;color:#888;font-size:13px;margin-bottom:4px">这个字的意思是？</div>`;
    optHtml=opts.map(o=>`<button class="quiz-opt" onclick="checkAnswerMeaning(this,'${target.char}','${o.char}')">${o.meaning}</button>`).join('');
  }
  quizState={target,pool};
  area.innerHTML=`
    ${question}
    <div class="quiz-options">${optHtml}</div>
    <div id="quiz-result" class="quiz-result"></div>
    <div style="text-align:center;margin-top:12px;display:none" id="quiz-next-btn">
      <button class="btn primary" onclick="startQuiz()">下一题</button>
      <button class="btn amber" onclick="openDetail(${target.id})" style="margin-left:8px">查看详情</button>
    </div>
  `;
}"""

new_show_quiz = """function showQuizQuestion(target,pool){
  let wrongOpts=shuffle(pool.filter(c=>c.char!==target.char)).slice(0,3);
  let opts=shuffle([target,...wrongOpts]);
  const area=document.getElementById('quiz-area');

  let question='',optHtml='';
  if(currentQuizType==='char2py'){
    question=`<div class="quiz-char">${target.char}</div><div style="text-align:center;color:#888;font-size:13px;margin-bottom:4px">这个字的读音是？</div>`;
    optHtml=opts.map(o=>`<button class="quiz-opt" onclick="checkAnswer(this,'${target.char}','${o.char}','${target.pinyin}','${o.pinyin}')">${o.pinyin}</button>`).join('');
    quizState={target,pool,type:'char2py'};
  }else if(currentQuizType==='py2char'){
    question=`<div class="quiz-char" style="font-size:40px;padding:20px 0">${target.pinyin}</div><div style="text-align:center;color:#888;font-size:13px;margin-bottom:4px">这个读音对应哪个汉字？</div>`;
    optHtml=opts.map(o=>`<button class="quiz-opt" onclick="checkAnswer(this,'${target.char}','${o.char}','${target.char}','${o.char}')">${o.char}</button>`).join('');
    quizState={target,pool,type:'py2char'};
  }else if(currentQuizType==='char2meaning'){
    question=`<div class="quiz-char">${target.char}</div><div style="text-align:center;color:#888;font-size:13px;margin-bottom:4px">这个字的意思是？</div>`;
    optHtml=opts.map(o=>`<button class="quiz-opt" onclick="checkAnswerMeaning(this,'${target.char}','${o.char}')">${o.meaning}</button>`).join('');
    quizState={target,pool,type:'char2meaning'};
  }else if(currentQuizType==='char2radical'){
    question=`<div class="quiz-char">${target.char}</div><div style="text-align:center;color:#888;font-size:13px;margin-bottom:4px">这个字的偏旁部首是？</div>`;
    optHtml=opts.map(o=>`<button class="quiz-opt" onclick="checkAnswerRadical(this,'${target.char}','${o.char}')">${o.radical||'?'}</button>`).join('');
    quizState={target,pool,type:'char2radical'};
  }else if(currentQuizType==='char2stroke'){
    question=`<div class="quiz-char">${target.char}</div><div style="text-align:center;color:#888;font-size:13px;margin-bottom:4px">这个字的笔画数是？</div>`;
    // For stroke count, generate reasonable distractor numbers (±1, ±2)
    let s=target.strokeCount||0;
    let distNums=[...new Set([s,Math.max(1,s-1),Math.max(1,s-2),s+1,s+2])].filter(n=>n>0).slice(0,4);
    let numOpts=shuffle(distNums.map(n=>({num:n,correct:n===s})));
    optHtml=numOpts.map(o=>`<button class="quiz-opt" onclick="checkAnswerStroke(this,'${target.char}','${target.strokeCount}',${o.num})">${o.num} 画</button>`).join('');
    quizState={target,pool,type:'char2stroke'};
  }
  area.innerHTML=`
    ${question}
    <div class="quiz-options">${optHtml}</div>
    <div id="quiz-result" class="quiz-result"></div>
    <div id="quiz-extra-info" style="text-align:center;margin-top:6px;display:none"></div>
    <div style="text-align:center;margin-top:12px;display:none" id="quiz-next-btn">
      <button class="btn primary" onclick="startQuiz()">下一题</button>
      <button class="btn amber" onclick="openDetail(${target.id})" style="margin-left:8px">查看详情</button>
    </div>
  `;
}"""

html = html.replace(old_show_quiz, new_show_quiz)

# 8. 新增 checkAnswerRadical 和 checkAnswerStroke 函数
# 在 checkAnswerMeaning 函数之后插入新函数
old_check_meaning_end = """function revealQuiz(el,targetChar,correct,chosenChar){"""

new_check_funcs = """function checkAnswerRadical(el,targetChar,chosenChar){
  if(!el.disabled){
    const entry=CHARS.find(c=>c.char===targetChar);
    const correct=(entry&&entry.radical===el.textContent);
    revealQuiz(el,targetChar,correct,chosenChar);
  }
}
function checkAnswerStroke(el,targetChar,targetStroke,chosenStroke){
  if(!el.disabled){
    const correct=(parseInt(chosenStroke)===parseInt(targetStroke));
    revealQuiz(el,targetChar,correct,targetChar);
  }
}
function revealQuiz(el,targetChar,correct,chosenChar){"""

html = html.replace(old_check_meaning_end, new_check_funcs)

# 9. 更新 revealQuiz 函数 - 添加部首/笔画信息展示
old_reveal = """function revealQuiz(el,targetChar,correct,chosenChar){
  document.querySelectorAll('.quiz-opt').forEach(b=>b.disabled=true);
  const entry=CHARS.find(c=>c.char===targetChar);
  if(correct){
    el.classList.add('correct');
    document.getElementById('quiz-result').className='quiz-result ok';
    document.getElementById('quiz-result').textContent='答对了！';
    markAsMastered(targetChar);
  }else{
    el.classList.add('wrong');
    document.querySelectorAll('.quiz-opt').forEach(b=>{
      if(b.textContent===entry.pinyin||b.textContent===entry.char||b.textContent===entry.meaning)b.classList.add('correct');
    });
    document.getElementById('quiz-result').className='quiz-result fail';
    document.getElementById('quiz-result').textContent=`答错了！正确答案是：${entry.pinyin} / ${entry.meaning}`;
    if(entry)markAsWrong(targetChar,entry);
    renderWrongList();
  }
  const nb=document.getElementById('quiz-next-btn');
  if(nb)nb.style.display='block';
  renderGrid();
}"""

new_reveal = """function revealQuiz(el,targetChar,correct,chosenChar){
  document.querySelectorAll('.quiz-opt').forEach(b=>b.disabled=true);
  const entry=CHARS.find(c=>c.char===targetChar);
  const extraInfo=document.getElementById('quiz-extra-info');
  if(correct){
    el.classList.add('correct');
    document.getElementById('quiz-result').className='quiz-result ok';
    document.getElementById('quiz-result').textContent='答对了！';
    markAsMastered(targetChar);
  }else{
    el.classList.add('wrong');
    document.querySelectorAll('.quiz-opt').forEach(b=>{
      if(b.textContent===entry.pinyin||b.textContent===entry.char||b.textContent===entry.meaning||b.textContent===entry.radical||(entry.strokeCount&&b.textContent===entry.strokeCount+' 画'))b.classList.add('correct');
    });
    document.getElementById('quiz-result').className='quiz-result fail';
    let correctInfo='';
    if(quizState.type==='char2radical')correctInfo=`部首：${entry.radical}`;
    else if(quizState.type==='char2stroke')correctInfo=`${entry.strokeCount} 画`;
    else correctInfo=`${entry.pinyin} / ${entry.meaning}`;
    document.getElementById('quiz-result').textContent=`答错了！正确答案：${correctInfo}`;
    if(entry)markAsWrong(targetChar,entry);
    renderWrongList();
  }
  // 展示部首和笔画信息
  if(entry&&extraInfo){
    extraInfo.style.display='block';
    extraInfo.innerHTML=`
      <div style="display:inline-flex;gap:16px;background:#e6f1fb;border-radius:10px;padding:8px 18px;font-size:13px;color:#185fa5;margin-top:4px">
        <span>部首：<b>${entry.radical||'?'}</b></span>
        <span>笔画：<b>${entry.strokeCount||'?'} 画</b></span>
      </div>`;
  }
  const nb=document.getElementById('quiz-next-btn');
  if(nb)nb.style.display='block';
  renderGrid();
}"""

html = html.replace(old_reveal, new_reveal)

# 10. 更新字详情弹窗 - 增加部首和笔画信息
old_detail_pinyin = """    <div class="detail-pinyin" id="d-pinyin"></div>
    <div class="detail-meaning" id="d-meaning"></div>"""

new_detail_pinyin = """    <div class="detail-pinyin" id="d-pinyin"></div>
    <div class="detail-meaning" id="d-meaning"></div>
    <div class="detail-radical-stroke" id="d-radical-stroke"></div>"""

html = html.replace(old_detail_pinyin, new_detail_pinyin)

# 11. 更新 openDetail 函数 - 增加部首笔画
old_open_detail = """function openDetail(id){
  const c=CHARS[id];
  currentDetailChar=c;
  document.getElementById('d-char').textContent=c.char;
  document.getElementById('d-pinyin').textContent=c.pinyin;
  document.getElementById('d-meaning').textContent=c.meaning;
  const reading=c.reading.replace(new RegExp(c.char,'g'),`<span class="key-char">${c.char}</span>`);
  document.getElementById('d-reading').innerHTML=reading;
  updateDetailStatus();
  document.getElementById('detail-overlay').classList.add('open');
}"""

new_open_detail = """function openDetail(id){
  const c=CHARS[id];
  currentDetailChar=c;
  document.getElementById('d-char').textContent=c.char;
  document.getElementById('d-pinyin').textContent=c.pinyin;
  document.getElementById('d-meaning').textContent=c.meaning;
  document.getElementById('d-radical-stroke').innerHTML=`
    <span class="radical-tag">部首：${c.radical||'?'}</span>
    <span class="stroke-tag">笔画：${c.strokeCount||'?'} 画</span>
  `;
  const reading=c.reading.replace(new RegExp(c.char,'g'),`<span class="key-char">${c.char}</span>`);
  document.getElementById('d-reading').innerHTML=reading;
  updateDetailStatus();
  document.getElementById('detail-overlay').classList.add('open');
}"""

html = html.replace(old_open_detail, new_open_detail)

# 12. 更新字库浏览格子 - 显示笔画数
old_render_grid = """  grid.innerHTML=list.map(c=>`
    <div class="char-cell${isMastered(c.char)?' mastered':''}${isWrong(c.char)?' wrong':''}" onclick="openDetail(${c.id})">
      <div class="grade-dot"></div>
      <span class="zi">${c.char}</span>
      <div class="py">${c.pinyin}</div>
    </div>
  `).join('');"""

new_render_grid = """  grid.innerHTML=list.map(c=>`
    <div class="char-cell${isMastered(c.char)?' mastered':''}${isWrong(c.char)?' wrong':''}" onclick="openDetail(${c.id})">
      <div class="grade-dot"></div>
      <span class="zi">${c.char}</span>
      <div class="py">${c.pinyin}</div>
      <div class="stroke-hint">${c.strokeCount||'?'}画</div>
    </div>
  `).join('');"""

html = html.replace(old_render_grid, new_render_grid)

# 13. 添加CSS样式
old_css_end = """  .metric .m-val.amber{color:#854f0b}
  @media(max-width:600px){"""

new_css = """  .metric .m-val.amber{color:#854f0b}
  .detail-radical-stroke{display:flex;gap:12px;justify-content:center;margin-bottom:12px}
  .radical-tag{background:#e6f1fb;color:#185fa5;border-radius:16px;padding:3px 12px;font-size:12px;font-weight:500}
  .stroke-tag{background:#faeeda;color:#854f0b;border-radius:16px;padding:3px 12px;font-size:12px;font-weight:500}
  .stroke-hint{font-size:10px;color:#aaa;text-align:center;margin-top:2px}
  .char-cell:hover .stroke-hint{color:#888}
  #quiz-extra-info{margin-top:8px}
  @media(max-width:600px){"""

html = html.replace(old_css_end, new_css)

# 14. 更新错题本显示 - 增加部首笔画
old_wrong_item = """    <div class="wrong-item" onclick="openDetail(${c.id})" style="cursor:pointer">
      <span class="wi-char">${c.char}</span>
      <div class="wi-info">
        <div style="font-size:14px;font-weight:500">${c.char}</div>
        <div class="wi-py">${c.pinyin}</div>
        <div class="wi-meaning">${c.meaning.slice(0,16)}…</div>
      </div>
      <span class="wi-cnt">错${getWrongCount(c.char)}次</span>
    </div>"""

new_wrong_item = """    <div class="wrong-item" onclick="openDetail(${c.id})" style="cursor:pointer">
      <span class="wi-char">${c.char}</span>
      <div class="wi-info">
        <div style="font-size:14px;font-weight:500">${c.char}</div>
        <div class="wi-py">${c.pinyin}</div>
        <div class="wi-meaning">部首:${c.radical||'?'} · ${c.strokeCount||'?'}画</div>
      </div>
      <span class="wi-cnt">错${getWrongCount(c.char)}次</span>
    </div>"""

html = html.replace(old_wrong_item, new_wrong_item)

# 写入
with open('C:/Users/Administrator/WorkBuddy/2026-06-02-task-5/识字训练应用.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('HTML updated successfully!')
print('Changes made:')
print('  1. Injected updated character database (7 fields)')
print('  2. Updated CHARS mapping with radical and strokeCount')
print('  3. Added 2 new quiz types: 字→部首, 字→笔画数')
print('  4. Added radical/stroke info display after quiz answers')
print('  5. Updated detail popup with radical and stroke tags')
print('  6. Updated character grid with stroke count hint')
print('  7. Updated wrong book display with radical/stroke info')
print('  8. Added CSS styles for new elements')
