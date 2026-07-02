// Generic whiteboard renderer. Reads comp/scene_timing.json where each scene has
// {id, start, end, type:"draw"|"slide"[, seed]}. Derives assets from id:
//   draw  -> scenes/<id>_color.png + scenes/<id>_lines.png
//   slide -> scenes/<id>.png
// Requires scene_full.html + hand.png beside this file (copied into <build>/comp/).
// Usage: node render.js            (run from the build's comp/ dir)
const PLAYWRIGHT = '/home/georgieporgie/claude_work/home-services-ad-toolkit/.claude/skills/image-studio/node_modules/playwright';
const { chromium } = require(PLAYWRIGHT);
const fs=require('fs'), path=require('path');
const DIR=__dirname, SC=path.join(DIR,'..','scenes'); const f=p=>'file://'+p;
const FPS=30;
const timing=JSON.parse(fs.readFileSync(path.join(DIR,'scene_timing.json')));
const cfg={
  hand:f(path.join(DIR,'hand.png')), handW:320, tip:{x:0.177,y:0.545},  // cartoon marker hand
  rightBound:0.80, art:{left:30,top:230,w:660,h:660}, duration:timing.duration,
  scenes: timing.scenes.map(s=>{
    const o={id:s.id, start:s.start, end:s.end, type:s.type, seed:s.seed};
    if(s.type==='draw'){ o.color=f(path.join(SC,s.id+'_color.png')); o.lines=f(path.join(SC,s.id+'_lines.png')); }
    else { o.img=f(path.join(SC,s.id+'.png')); }
    return o;
  })
};
(async()=>{
  const out=path.join(DIR,'frames'); fs.rmSync(out,{recursive:true,force:true}); fs.mkdirSync(out,{recursive:true});
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:720,height:1280},deviceScaleFactor:1});
  await p.goto(f(path.join(DIR,'scene_full.html')));
  await p.evaluate(c=>window.init(c), cfg);
  await p.evaluate(()=>window.__ready); await p.waitForTimeout(400);
  const N=Math.ceil(timing.duration*FPS);
  console.log('rendering',N,'frames');
  for(let i=0;i<N;i++){ await p.evaluate(tt=>window.render(tt), i/FPS);
    await p.screenshot({path:path.join(out,String(i).padStart(5,'0')+'.png')});
    if(i%150===0) console.log('  '+i+'/'+N); }
  await b.close(); console.log('frames done', N);
})();
