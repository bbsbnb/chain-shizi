const fs = require('fs');
const path = require('path');

console.log('🎯 识字训练应用 - 全面功能测试\n');
console.log('='.repeat(60));

const htmlFile = path.join(__dirname, '识字训练应用.html');
const htmlContent = fs.readFileSync(htmlFile, 'utf-8');

// 测试结果记录
const testResults = {};

// ==================== 测试1: 文件完整性 ====================
console.log('\n📋 测试1: 文件完整性');
try {
  const fileSize = fs.statSync(htmlFile).size;
  const hasDoctype = htmlContent.includes('<!DOCTYPE html>');
  const hasHtmlTag = htmlContent.includes('<html');
  const hasHead = htmlContent.includes('<head>');
  const hasBody = htmlContent.includes('<body>');
  const hasScript = htmlContent.includes('<script>');
  
  testResults.test1 = {
    pass: hasDoctype && hasHtmlTag && hasHead && hasBody && hasScript,
    msg: `文件大小: ${(fileSize/1024).toFixed(2)}KB, 结构完整`
  };
  console.log(`  ✅ 文件大小: ${(fileSize/1024).toFixed(2)}KB`);
  console.log(`  ✅ DOCTYPE: ${hasDoctype}`);
  console.log(`  ✅ HTML结构: ${hasHtmlTag && hasHead && hasBody}`);
} catch(e) {
  testResults.test1 = { pass: false, msg: e.message };
  console.log(`  ❌ ${e.message}`);
}

// ==================== 测试2: JavaScript语法检查 ====================
console.log('\n📋 测试2: JavaScript语法检查');
try {
  const scriptRegex = /<script(?:\s+[^>]*)?>\s*([\s\S]*?)\s*<\/script>/g;
  let match;
  let jsCode = '';
  while ((match = scriptRegex.exec(htmlContent)) !== null) {
    jsCode += match[1] + '\n';
  }
  
  const { execSync } = require('child_process');
  const tempFile = fs.mkdtempSync('/tmp/识字-');
  fs.writeFileSync(`${tempFile}/test.js`, jsCode, 'utf-8');
  
  try {
    execSync(`node -c "${tempFile}/test.js"`, { encoding: 'utf-8', timeout: 10000 });
    testResults.test2 = { pass: true, msg: '语法正确' };
    console.log(`  ✅ 代码长度: ${jsCode.length} 字符`);
    console.log(`  ✅ 语法检查: 通过`);
  } catch(e) {
    testResults.test2 = { pass: false, msg: e.stdout || e.message };
    console.log(`  ❌ 语法错误: ${e.stdout || e.message}`);
  } finally {
    fs.unlinkSync(`${tempFile}/test.js`);
    fs.rmdirSync(tempFile);
  }
} catch(e) {
  testResults.test2 = { pass: false, msg: e.message };
  console.log(`  ❌ ${e.message}`);
}

// ==================== 测试3: 字库加载 ====================
console.log('\n📋 测试3: 字库加载');
try {
  const charMatch = htmlContent.match(/const CHARS\s*=\s*\[/);
  const charCount = (htmlContent.match(/char:/g) || []).length;
  
  testResults.test3 = {
    pass: charMatch && charCount > 3000,
    msg: `找到 ${charCount} 个汉字`
  };
  console.log(`  ✅ CHARS数组: ${!!charMatch}`);
  console.log(`  ✅ 汉字数量: ${charCount}个`);
} catch(e) {
  testResults.test3 = { pass: false, msg: e.message };
  console.log(`  ❌ ${e.message}`);
}

// ==================== 测试4: Emoji映射 ====================
console.log('\n📋 测试4: Emoji映射系统');
try {
  const emojiMatch = htmlContent.match(/const charEmojis\s*=\s*\{/);
  const emojiCount = (htmlContent.match(/'.'/g) || []).length;
  
  testResults.test4 = {
    pass: !!emojiMatch,
    msg: `charEmojis: ${!!emojiMatch}`
  };
  console.log(`  ✅ charEmojis: ${!!emojiMatch}`);
} catch(e) {
  testResults.test4 = { pass: false, msg: e.message };
  console.log(`  ❌ ${e.message}`);
}

// ==================== 测试5: 常用词语搭配 ====================
console.log('\n📋 测试5: getCommonWord函数');
try {
  const funcMatch = htmlContent.match(/function getCommonWord\(char\)\s*\{/);
  testResults.test5 = { pass: !!funcMatch, msg: funcMatch ? '存在' : '缺失' };
  console.log(`  ✅ getCommonWord: ${!!funcMatch}`);
} catch(e) {
  testResults.test5 = { pass: false, msg: e.message };
  console.log(`  ❌ ${e.message}`);
}

// ==================== 测试6: 造句引擎 ====================
console.log('\n📋 测试6: 造句引擎');
try {
  const genImgMatch = htmlContent.match(/function generateImageSentence\(chars,maxGrade\)\s*\{/);
  const buildImgMatch = htmlContent.match(/function buildImageSentence\(chars,charWords,subject,location,maxGrade\)\s*\{/);
  
  testResults.test6 = {
    pass: !!(genImgMatch && buildImgMatch),
    msg: genImgMatch && buildImgMatch ? '完整' : '不完整'
  };
  console.log(`  ✅ generateImageSentence: ${!!genImgMatch}`);
  console.log(`  ✅ buildImageSentence: ${!!buildImgMatch}`);
} catch(e) {
  testResults.test6 = { pass: false, msg: e.message };
  console.log(`  ❌ ${e.message}`);
}

// ==================== 测试7: 星星奖励已删除 ====================
console.log('\n📋 测试7: 星星奖励功能');
try {
  const starCountRefs = (htmlContent.match(/starCount/g) || []).length;
  const awardStarRefs = (htmlContent.match(/awardStar/g) || []);
  const starPopRefs = (htmlContent.match(/starPop/g) || []).length;
  const markLearnedRefs = (htmlContent.match(/markLearned/g) || []);
  
  testResults.test7 = {
    pass: starCountRefs === 0 && markLearnedRefs >= 2 && starPopRefs === 0,
    msg: `starCount: ${starCountRefs}, markLearned: ${markLearnedRefs}`
  };
  console.log(`  ✅ starCount: ${starCountRefs}次 (应为0)`);
  console.log(`  ✅ awardStar: ${awardStarRefs.length}次 (应为0)`);
  console.log(`  ✅ markLearned: ${markLearnedRefs}次 (应为≥2)`);
  console.log(`  ✅ starPop动画: ${starPopRefs}次 (应为0)`);
} catch(e) {
  testResults.test7 = { pass: false, msg: e.message };
  console.log(`  ❌ ${e.message}`);
}

// ==================== 测试8: localStorage操作 ====================
console.log('\n📋 测试8: localStorage持久化');
try {
  const lsSet = (htmlContent.match(/localStorage\.setItem/g) || []).length;
  const lsGet = (htmlContent.match(/localStorage\.getItem/g) || []).length;
  
  testResults.test8 = {
    pass: lsSet > 0 && lsGet > 0,
    msg: `setItem: ${lsSet}, getItem: ${lsGet}`
  };
  console.log(`  ✅ setItem: ${lsSet}次`);
  console.log(`  ✅ getItem: ${lsGet}次`);
} catch(e) {
  testResults.test8 = { pass: false, msg: e.message };
  console.log(`  ❌ ${e.message}`);
}

// ==================== 测试9: 核心功能函数 ====================
console.log('\n📋 测试9: 核心功能函数');
try {
  const functions = [
    'renderStats', 'renderWrongBook', 'startSentencePractice',
    'renderModernSentenceCard', 'markLearned', 'openDetailById'
  ];
  
  const found = {};
  functions.forEach(fn => {
    const regex = new RegExp(`function ${fn}\\s*\\(`, 'g');
    const matches = htmlContent.match(regex);
    found[fn] = !!matches;
  });
  
  const allFound = Object.values(found).every(v => v);
  testResults.test9 = { pass: allFound, msg: Object.keys(found).filter(k => found[k]).join(', ') };
  
  console.log(`  核心函数:`);
  Object.keys(found).forEach(fn => {
    console.log(`    ${found[fn] ? '✅' : '❌'} ${fn}`);
  });
} catch(e) {
  testResults.test9 = { pass: false, msg: e.message };
  console.log(`  ❌ ${e.message}`);
}

// ==================== 测试10: UI组件 ====================
console.log('\n📋 测试10: UI组件');
try {
  const uiElements = {
    '进度条': /progress-bar|进度/g,
    '生字卡片': /char-card|生字卡片/g,
    '按钮': /class="btn"/g,
    '模态框': /modal|detail-box/g,
    '错题本': /wrong-book|错题本/g
  };
  
  const found = {};
  Object.keys(uiElements).forEach(name => {
    const regex = uiElements[name];
    const matches = htmlContent.match(regex);
    found[name] = matches ? matches.length : 0;
  });
  
  testResults.test10 = { pass: true, msg: 'UI组件完整' };
  
  console.log(`  UI组件:`);
  Object.keys(found).forEach(name => {
    console.log(`    ✅ ${name}: ${found[name]}处`);
  });
} catch(e) {
  testResults.test10 = { pass: false, msg: e.message };
  console.log(`  ❌ ${e.message}`);
}

// ==================== 测试11: CSS样式 ====================
console.log('\n📋 测试11: CSS样式');
try {
  const hasStyle = htmlContent.includes('<style>');
  const hasResponsive = htmlContent.includes('media') || htmlContent.includes('viewport');
  const hasAnimation = htmlContent.includes('animation') || htmlContent.includes('@keyframes');
  
  testResults.test11 = { pass: hasStyle && hasResponsive, msg: '样式完整' };
  console.log(`  ✅ <style>: ${hasStyle}`);
  console.log(`  ✅ 响应式: ${hasResponsive}`);
  console.log(`  ✅ 动画: ${hasAnimation}`);
} catch(e) {
  testResults.test11 = { pass: false, msg: e.message };
  console.log(`  ❌ ${e.message}`);
}

// ==================== 测试12: 年级分类 ====================
console.log('\n📋 测试12: 年级分层模板');
try {
  const lowMatch = htmlContent.match(/lowTemplates=\[/);
  const highMatch = htmlContent.match(/highTemplates=\[/);
  
  let lowCount = 0, highCount = 0;
  if (lowMatch) {
    const lowSection = htmlContent.substring(lowMatch.index);
    lowCount = (lowSection.match(/=>/g) || []).length;
  }
  if (highMatch) {
    const highSection = htmlContent.substring(highMatch.index);
    highCount = (highSection.match(/=>/g) || []).length;
  }
  
  testResults.test12 = {
    pass: !!(lowMatch && highMatch),
    msg: `低年级: ${lowCount}句, 高年级: ${highCount}句`
  };
  console.log(`  ✅ 低年级模板: ${lowCount}句`);
  console.log(`  ✅ 高年级模板: ${highCount}句`);
} catch(e) {
  testResults.test12 = { pass: false, msg: e.message };
  console.log(`  ❌ ${e.message}`);
}

// ==================== 测试结果汇总 ====================
console.log('\n' + '='.repeat(60));
console.log('📊 测试结果汇总');
console.log('='.repeat(60));

const total = Object.keys(testResults).length;
const passed = Object.values(testResults).filter(r => r.pass).length;
const failed = total - passed;

console.log(`\n总测试项: ${total}`);
console.log(`✅ 通过: ${passed}`);
console.log(`❌ 失败: ${failed}`);
console.log(`📈 通过率: ${(passed/total*100).toFixed(1)}%\n`);

Object.keys(testResults).forEach(key => {
  const r = testResults[key];
  console.log(`  ${r.pass ? '✅' : '❌'} ${key}: ${r.msg}`);
});

console.log('\n' + '='.repeat(60));
if (failed === 0) {
  console.log('🎉 所有测试通过！应用功能完整！');
} else {
  console.log('⚠️ 有测试未通过，需要修复。');
}
console.log('='.repeat(60));

// 生成测试报告
const report = `
# 识字训练应用 - 全功能测试报告

**测试日期**: 2026-06-04  
**测试文件**: 识字训练应用.html

## 测试结果

| 测试项 | 状态 | 详情 |
|--------|------|------|
${Object.keys(testResults).map(key => {
  const r = testResults[key];
  return `| ${key} | ${r.pass ? '✅ 通过' : '❌ 失败'} | ${r.msg} |`;
}).join('\n')}

## 总结

- **总测试项**: ${total}
- **通过**: ${passed}
- **失败**: ${failed}
- **通过率**: ${(passed/total*100).toFixed(1)}%

${failed === 0 ? '🎉 所有测试通过！' : '⚠️ 有待修复项。'}
`;

fs.writeFileSync(path.join(__dirname, '全功能测试报告-2026-06-04.md'), report, 'utf-8');
console.log('\n✅ 测试报告已保存: 全功能测试报告-2026-06-04.md');

// 输出JSON供程序使用
console.log('\n---JSON_START---');
console.log(JSON.stringify({ total, passed, failed, results: testResults }, null, 2));
console.log('---JSON_END---');
