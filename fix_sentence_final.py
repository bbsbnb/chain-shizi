# 形象互动版造句专练 - 重写
import re

with open('识字训练应用.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 形象互动版完整代码
new_code = r'''// ====================== 形象互动版造句专练 ======================
let sentencePracticeData=[];
let sentenceIndex=0;
let starCount=0;
let usedCombinations=new Set();
let usedSentences=new Set();

// 汉字Emoji映射表（让生字更形象）
const charEmojis={
  '跑':'🏃','跳':'🤸','吃':'🍚','喝':'🥤','看':'👀','说':'💬','笑':'😊','玩':'🎮',
  '学':'📚','校':'🏫','老':'👴','师':'👨‍🏫','同':'👫','爷':'👴','奶':'👵','哥':'👦',
  '姐':'👧','弟':'👶','妹':'👶','爸':'👨','妈':'👩','天':'☀️','气':'💨','春':'🌸',
  '夏':'☀️','秋':'🍂','冬':'❄️','花':'🌺','草':'🌿','树':'🌳','水':'💧','火':'🔥',
  '山':'⛰️','石':'🪨','日':'☀️','月':'🌙','星':'⭐','云':'☁️','风':'🌬️','雨':'🌧️',
  '雪':'❄️','电':'💡','话':'🗣️','书':'📖','文':'📝','字':'✏️','数':'🔢','音':'🎵',
  '美':'✨','术':'🎨','体':'⚽','游':'🎲','狗':'🐕','猫':'🐱','鸟':'🐦','鱼':'🐟',
  '马':'🐴','牛':'🐄','羊':'🐑','猪':'🐷','鸡':'🐔','鸭':'🦆','鹅':'🦢','兔':'🐰',
  '苹果':'🍎','香蕉':'🍌','米饭':'🍚','面条':'🍜','西瓜':'🍉','糖果':'🍬',
  '家':'🏠','学校':'🏫','公园':'🌳','超市':'🛒','医院':'🏥','车站':'🚌',
  '走':'🚶','飞':'🕊️','游':'🏊','爬':'🧗','滑':'⛸️','听':'👂','读':'📖','画':'🎨',
  '买':'🛍️','做':'🔨','开':'🚗','拿':'🤲','放':'📦','打':'🔨','帮':'🤝','送':'🎁',
  '找':'🔍','叫':'📢','喊':'📣','洗':'🧼','刷':'🪥','穿':'👕','睡':'😴','起':'⬆️',
};

function getCharEmoji(char){
  return charEmojis[char]||'📝';
}

function shuffle(arr){
  const a=[...arr];
  for(let i=a.length-1;i>0;i--){
    const j=Math.floor(Math.random()*(i+1));
    [a[i],a[j]]=[a[j],a[i]];
  }
  return a;
}

function getComboKey(chars){
  return [...chars].map(c=>c.char).sort().join('');
}

function startSentencePractice(){
  const wrongList=Object.values(wrongBook).map(w=>CHARS.find(c=>c.char===w.char)).filter(Boolean);
  if(wrongList.length<2){
    alert('至少需要2个错题才能生成造句练习！');
    return;
  }
  
  // 固定选取2个字组合造句（更聚焦）
  const batchSize=2;
  
  sentencePracticeData=[];
  starCount=0;
  usedCombinations.clear();
  usedSentences.clear();
  let attempts=0;
  
  for(let batch=0;batch<5;batch++){
    let batchChars;
    let comboKey;
    let found=false;
    
    while(attempts<100){
      const shuffled=shuffle(wrongList);
      batchChars=shuffled.slice(0,Math.min(batchSize,wrongList.length));
      comboKey=getComboKey(batchChars);
      
      if(!usedCombinations.has(comboKey)){
        found=true;
        usedCombinations.add(comboKey);
        break;
      }
      attempts++;
    }
    
    if(!found){
      usedCombinations.clear();
      batchChars=shuffle(wrongList).slice(0,batchSize);
      comboKey=getComboKey(batchChars);
      usedCombinations.add(comboKey);
    }
    
    const maxGrade=Math.max(...batchChars.map(c=>c.grade||1));
    
    let sentence;
    let sentenceKey;
    attempts=0;
    
    while(attempts<50){
      sentence=generateImageSentence(batchChars,maxGrade);
      sentenceKey=sentence.trim();
      
      if(!usedSentences.has(sentenceKey)){
        usedSentences.add(sentenceKey);
        break;
      }
      attempts++;
    }
    
    sentencePracticeData.push({
      chars:batchChars.map(c=>({char:c.char,pinyin:c.pinyin,meaning:c.meaning,grade:c.grade})),
      sentence:sentence,
      scene:getSceneDescription(maxGrade),
      maxGrade:maxGrade
    });
  }
  
  sentenceIndex=0;
  const area=document.getElementById('sentence-practice-area');
  area.style.display='block';
  area.className='sentence-practice-modern';
  renderModernSentenceCard();
  
  area.scrollIntoView({behavior:'smooth'});
}

function getSceneDescription(grade){
  const scenes={
    low:['🌈 彩虹桥上','🌳 大树底下','🏞️ 小河旁边','🌻 花园里','🏠 家里客厅','🛒 超市货架前'],
    high:['📚 图书馆里','🏟️ 运动场上','🌃 夜晚星空下','🎪 游乐园中','🏛️ 博物馆里','🌊 海滩边上']
  };
  const pool=grade<=2?scenes.low:scenes.high;
  return pool[Math.floor(Math.random()*pool.length)];
}

// 形象造句引擎
function generateImageSentence(chars,maxGrade){
  const charData=chars.map(c=>({char:c.char,pinyin:c.pinyin,meaning:c.meaning,grade:c.grade}));
  const charCount=charData.length;
  const targetLen=maxGrade<=2?14:20;
  
  const charWords=charData.map(c=>getCommonWord(c.char));
  const emojis=charData.map(c=>getCharEmoji(c.char));
  const scene=maxGrade<=2?getScene('low'):getScene('high');
  const verb=scene.verbs[Math.floor(Math.random()*scene.verbs.length)];
  const subject=scene.subjects[Math.floor(Math.random()*scene.subjects.length)];
  const location=scene.locations?scene.locations[Math.floor(Math.random()*scene.locations.length)]:'';
  const connector=scene.connectors[Math.floor(Math.random()*scene.connectors.length)];
  
  return buildImageSentence(charData,charWords,emojis,subject,verb,location,connector,targetLen,maxGrade);
}

function buildImageSentence(chars,charWords,emojis,subject,verb,location,connector,targetLen,maxGrade){
  const c1=charWords[0],c2=charWords[1];
  const e1=emojis[0],e2=emojis[1];
  
  // 趣味性模板库（2字组合，更生动有趣）
  const funTemplates=[
    // 故事型
    ()=>`${subject}正在${verb}${c1}${e1}，${connector}${c2}${e2}也跑来了！`,
    ()=>`看！${subject}在${location}${verb}${c1}${e1}呢，${c2}${e2}看见了赶紧过来。`,
    // 对话型
    ()=>`${subject}说："来玩${verb}${c1}${e1}吧！"${c2}${e2}笑着跑过来。`,
    ()=>`${subject}对${c1}${e1}说："快来${verb}${c2}${e2}！"`,
    // 发现型
    ()=>`在${location}，${subject}发现${c1}${e1}和${c2}${e2}在一起！`,
    ()=>`今天天气真好！${subject}带着${c1}${e1}去找${c2}${e2}玩。`,
    // 友情型
    ()=>`${c1}${e1}和${c2}${e2}是一对好朋友，他们${connector}${subject}一起${verb}。`,
    ()=>`${c1}${e1}和${c2}${e2}手拉手，${connector}${subject}一起${verb}。`,
    // 惊喜型
    ()=>`哇！${c1}${e1}和${c2}${e2}，${subject}全找到了！`,
    ()=>`太棒了！${subject}找到${c1}${e1}和${c2}${e2}了！`,
    // 动作型
    ()=>`${verb}${c1}${e1}，${c2}${e2}也跟着来了，${subject}真开心。`,
    ()=>`${subject}带着${c1}${e1}去${verb}，${c2}${e2}也追着来了。`,
  ];
  
  let s=funTemplates[Math.floor(Math.random()*funTemplates.length)]();
  return adjustLen(s,targetLen);
}

// 根据汉字获取常用词语搭配
function getCommonWord(char){
  const pairs={
    '跑':'跑步','跳':'跳绳','吃':'吃饭','喝':'喝水',
    '看':'看书','说':'说话','笑':'笑话','玩':'玩具',
    '学':'上学','校':'学校','老':'老师','师':'老师',
    '同':'同学','爷':'爷爷','奶':'奶奶','哥':'哥哥',
    '姐':'姐姐','弟':'弟弟','妹':'妹妹','爸':'爸爸',
    '妈':'妈妈','天':'天气','气':'气球','春':'春天',
    '夏':'夏天','秋':'秋天','冬':'冬天','花':'花朵',
    '草':'小草','树':'大树','水':'水','火':'火车',
    '山':'大山','石':'石头','日':'日子','月':'月亮',
    '星':'星星','云':'白云','风':'大风','雨':'下雨',
    '雪':'雪花','电':'电脑','话':'说话','书':'书本',
    '文':'语文','字':'写字','数':'数学','音':'音乐',
    '美':'美丽','术':'美术','体':'体育','游':'游戏',
  };
  return pairs[char]||(char+'子');
}

// 获取场景配置
function getScene(level){
  if(level==='low'){
    return{
      subjects:['我','我们','小明','小红','小狗','小猫','弟弟','妹妹'],
      verbs:['跑','跳','走','看','玩','找','拿','吃','喝','说'],
      locations:['家里','学校','公园','操场','超市','路上'],
      connectors:['和','跟','一起']
    };
  }
  return{
    subjects:['我','我们','同学们','老师','哥哥','姐姐'],
    verbs:['跑','跳','走','看','说','写','读','学','做','帮'],
    locations:['学校里','操场上','公园里','街道上','教室'],
    connectors:['和','跟','一起','然后','于是']
  };
}

// 调整句子长度
function adjustLen(sentence,targetLen){
  const diff=sentence.length-targetLen;
  if(diff>8){
    if(sentence.includes('在')){
      sentence=sentence.replace(/在[^，。！？]*，?/,'');
    }
  }
  if(diff<-8){
    const ext=['，大家很开心。','，真好玩。','，笑得真开心。'];
    sentence+=ext[Math.floor(Math.random()*ext.length)];
  }
  return sentence;
}

// 渲染现代化造句卡片
function renderModernSentenceCard(){
  const area=document.getElementById('sentence-practice-area');
  
  if(sentenceIndex>=sentencePracticeData.length){
    area.innerHTML=`
      <div class="sentence-card-modern" style="text-align:center;padding:40px 20px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;border-radius:16px;">
        <div style="font-size:48px;margin-bottom:20px">🎉</div>
        <div style="font-size:24px;font-weight:bold;margin-bottom:10px">太棒了！</div>
        <div style="font-size:18px;margin-bottom:20px">你已经完成了所有造句练习！</div>
        <div style="font-size:32px;margin:20px 0">⭐ ${starCount} 颗星</div>
        <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
          <button class="btn" style="background:#fff;color:#667eea;padding:12px 24px;border-radius:8px;font-size:16px;font-weight:bold;border:none;cursor:pointer" onclick="startSentencePractice()">🔄 再来一次</button>
          <button class="btn" style="background:rgba(255,255,255,0.2);color:#fff;padding:12px 24px;border-radius:8px;font-size:16px;border:2px solid #fff;cursor:pointer" onclick="document.getElementById('sentence-practice-area').style.display='none'">✕ 返回列表</button>
        </div>
      </div>
    `;
    return;
  }
  
  const data=sentencePracticeData[sentenceIndex];
  const total=sentencePracticeData.length;
  const charCount=data.chars.length;
  
  // 构建生字形象卡片
  const charCards=data.chars.map((c,i)=>{
    const emoji=getCharEmoji(c.char);
    return `
      <div class="char-bubble" style="display:inline-flex;flex-direction:column;align-items:center;margin:8px;padding:12px;background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.1);cursor:pointer;transition:all 0.3s;min-width:80px" onclick="openDetailById('${c.char}')" onmouseover="this.style.transform='translateY(-5px)';this.style.boxShadow='0 4px 16px rgba(0,0,0,0.2)'" onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 2px 8px rgba(0,0,0,0.1)'">
        <div style="font-size:32px;margin-bottom:4px">${emoji}</div>
        <div style="font-size:28px;font-weight:bold;color:#185fa5;margin-bottom:2px">${c.char}</div>
        <div style="font-size:12px;color:#888;margin-bottom:2px">${c.pinyin}</div>
        <div style="font-size:11px;color:#5f5e5a;text-align:center">${c.meaning}</div>
      </div>
    `;
  }).join('');
  
  // 高亮句子中的生字
  let highlightedSentence=data.sentence;
  data.chars.forEach(c=>{
    const escaped=c.char.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
    highlightedSentence=highlightedSentence.replace(new RegExp(escaped,'g'),`<span style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;padding:2px 6px;border-radius:4px;font-weight:bold;cursor:pointer" onclick="openDetailById('${c.char}')">${c.char}</span>`);
  });
  
  area.innerHTML=`
    <div class="sentence-card-modern" style="background:#fff;border-radius:16px;box-shadow:0 4px 20px rgba(0,0,0,0.1);overflow:hidden">
      <!-- 头部进度条 -->
      <div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:16px 20px;color:#fff">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
          <span style="font-size:14px;opacity:0.9">第 ${sentenceIndex+1}/${total} 题</span>
          <span style="font-size:14px">⭐ ${starCount} 星</span>
        </div>
        <div style="height:6px;background:rgba(255,255,255,0.3);border-radius:3px;overflow:hidden">
          <div style="height:100%;width:${(sentenceIndex+1)/total*100}%;background:#fff;border-radius:3px;transition:width 0.3s"></div>
        </div>
      </div>
      
      <!-- 场景描述 -->
      <div style="padding:16px 20px;background:#f8f9fa;border-bottom:2px dashed #e0e0e0">
        <div style="font-size:16px;color:#666">🎬 场景：${data.scene}</div>
      </div>
      
      <!-- 生字展示区 -->
      <div style="padding:20px;background:#fafbfc">
        <div style="font-size:13px;color:#888;margin-bottom:12px;font-weight:bold">📖 生字宝宝（点击查看详情）</div>
        <div style="display:flex;flex-wrap:wrap;justify-content:center">${charCards}</div>
      </div>
      
      <!-- 句子展示区 -->
      <div style="padding:20px">
        <div style="font-size:13px;color:#888;margin-bottom:12px;font-weight:bold">💭 造句时间</div>
        <div style="background:linear-gradient(135deg,#f5f7fa 0%,#c3cfe2 100%);padding:20px;border-radius:12px;font-size:20px;line-height:1.8;color:#333;text-align:center;min-height:60px;display:flex;align-items:center;justify-content:center">${highlightedSentence}</div>
      </div>
      
      <!-- 操作按钮 -->
      <div style="padding:20px;background:#f8f9fa;border-top:1px solid #e0e0e0">
        <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center">
          ${sentenceIndex>0?`<button class="btn" style="flex:1;min-width:120px;padding:12px;border-radius:8px;border:none;background:#e0e0e0;cursor:pointer;font-size:14px" onclick="sentenceIndex--;renderModernSentenceCard()">⬅️ 上一题</button>`:'<div style="flex:1;min-width:120px"></div>'}
          <button class="btn" style="flex:2;min-width:160px;padding:12px;border-radius:8px;border:none;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;cursor:pointer;font-size:14px;font-weight:bold" onclick="awardStar()">⭐ 获得星星</button>
          <button class="btn primary" style="flex:1;min-width:120px;padding:12px;border-radius:8px;border:none;background:#185fa5;color:#fff;cursor:pointer;font-size:14px" onclick="sentenceIndex++;renderModernSentenceCard()">➡️ 下一题</button>
        </div>
      </div>
    </div>
  `;
}

// 获得星星奖励
function awardStar(){
  starCount++;
  const area=document.getElementById('sentence-practice-area');
  const starEffect=document.createElement('div');
  starEffect.style.cssText='position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);font-size:80px;z-index:9999;animation:starPop 1s ease-out forwards;pointer-events:none';
  starEffect.textContent='⭐';
  document.body.appendChild(starEffect);
  setTimeout(()=>starEffect.remove(),1000);
  
  setTimeout(()=>{
    if(sentenceIndex<sentencePracticeData.length-1){
      sentenceIndex++;
      renderModernSentenceCard();
    }else{
      renderModernSentenceCard();
    }
  },800);
}

// 添加CSS动画
if(!document.getElementById('sentence-animations')){
  const style=document.createElement('style');
  style.id='sentence-animations';
  style.textContent=`
    @keyframes starPop{
      0%{transform:translate(-50%,-50%) scale(0) rotate(0deg);opacity:1}
      50%{transform:translate(-50%,-50%) scale(1.5) rotate(180deg);opacity:1}
      100%{transform:translate(-50%,-50%) scale(2) rotate(360deg);opacity:0}
    }
    @keyframes bounce{
      0%,100%{transform:translateY(0)}
      50%{transform:translateY(-10px)}
    }
    .char-bubble{animation:bounce 2s ease-in-out infinite}
    .char-bubble:nth-child(2){animation-delay:0.2s}
    .char-bubble:nth-child(3){animation-delay:0.4s}
    .char-bubble:nth-child(4){animation-delay:0.6s}
    .char-bubble:nth-child(5){animation-delay:0.8s}
  `;
  document.head.appendChild(style);
}

function openDetailById(char){
  const c=CHARS.find(x=>x.char===char);
  if(c)openDetail(c.id);
}
'''

# 从 'let sentencePracticeData' 到 'function openDetailById(char)' 结束
pattern = r'// ====================== 造句专练[^\n]*\nlet sentencePracticeData\[\];[\s\S]*?function openDetailById\(char\)\{[\s\S]*?\}'

new_content = re.sub(pattern, new_code.strip(), content)

with open('识字训练应用.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Done! Image sentence practice replaced successfully.')
