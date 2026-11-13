// Offline/online Chromium CDP smoke for GitHub Pages (Windows / Node 24).
// Separate headless profile: never touches existing user desktop sessions/tabs.
"use strict";
const fs=require("fs"), path=require("path"),os=require("os"),{spawn}=require("child_process");
const target=process.argv[2] || "https://trinhtanphat.github.io/hsg-tin-12-kim-lien-2023-2024/";
const chrome="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const profile=fs.mkdtempSync(path.join(os.tmpdir(),"kimlien-chrome-"));
const screenshots=path.join(os.tmpdir(),"kimlien-pages-audit");
fs.mkdirSync(screenshots,{recursive:true});
const child=spawn(chrome,["--headless=new","--disable-gpu","--no-first-run","--no-default-browser-check","--disable-extensions","--disable-background-networking","--remote-debugging-port=0","--user-data-dir="+profile,"--window-size=1440,900","about:blank"],{stdio:"ignore"});
const sleep=t=>new Promise(r=>setTimeout(r,t));
async function waitPort(){const p=path.join(profile,"DevToolsActivePort");for(let i=0;i<130;i++){if(fs.existsSync(p)){const lines=fs.readFileSync(p,"utf8").trim().split(/\r?\n/);return Number(lines[0]);}await sleep(100)}throw Error("Chrome DevTools port unavailable");}
let ws,next=1,pending=new Map(),errors=[];
function send(method,params={}){return new Promise((resolve,reject)=>{const id=next++;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));setTimeout(()=>{if(pending.has(id)){pending.delete(id);reject(Error("CDP timeout: "+method))}},20000)})}
async function evalJs(expression){const r=await send("Runtime.evaluate",{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error("JS exception: "+JSON.stringify(r.exceptionDetails));return r.result?.value}
async function main(){
 if(!fs.existsSync(chrome))throw Error("Chrome not found");
 const port=await waitPort();const pages=await(await fetch("http://127.0.0.1:"+port+"/json/list")).json();
 const page=pages.find(p=>p.type==="page");if(!page)throw Error("No Chrome page");
 ws=new WebSocket(page.webSocketDebuggerUrl);
 await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject});
 ws.onmessage=e=>{const x=JSON.parse(e.data);if(x.id&&pending.has(x.id)){const p=pending.get(x.id);pending.delete(x.id);return x.error?p.reject(Error(JSON.stringify(x.error))):p.resolve(x.result)}if(x.method==="Runtime.exceptionThrown")errors.push(x.params.exceptionDetails?.text)};
 await send("Page.enable");await send("Runtime.enable");
 const load=await send("Page.navigate",{url:target});if(load.errorText)throw Error(load.errorText);await sleep(3500);
 await evalJs("(async()=>{const imgs=[...document.images];for(const img of imgs){img.loading='eager'}return Promise.all(imgs.map(x=>x.decode().then(()=>true,()=>false)))})()");
 const summary=await evalJs("({title:document.title,sections:document.querySelectorAll('section').length,cards:document.querySelectorAll('.problem-card').length,tabs:document.querySelectorAll('[data-lab]').length,images:[...document.images].map(x=>({ok:x.complete&&x.naturalWidth>0,url:x.currentSrc})),host:location.host})");
 if(summary.cards!==5||summary.tabs!==5||summary.sections<5||summary.images.some(x=>!x.ok))throw Error("Missing sections/cards/images "+JSON.stringify(summary));
 const links=await evalJs("[...document.querySelectorAll('a[href]')].map(x=>x.getAttribute('href')).filter(h=>h.startsWith('./')&&/\\.(?:zip|pdf|docx|png)$/.test(h))");
 for(const link of links){const res=await fetch(new URL(link,target),{method:"HEAD"});if(!res.ok)throw Error("Broken downloadable link "+link+" HTTP "+res.status)}
 const expect={PRIME:"YES",PROTEIN:"Ser-Ser-His-Arg-Gly",BILLARD:"6 4",DIVIDE:"9",ALKANE:"3"};
 for(const [key,want] of Object.entries(expect)){
  const got=await evalJs("document.querySelector('[data-lab=\\\""+key+"\\\"]').click();document.querySelector('#lab-result').textContent.trim()");
  if(got!==want)throw Error(key+" expected "+want+" got "+got);
 }
 const detail=await evalJs("document.querySelector('[data-problem=ALKANE]').click();({meta:document.querySelector('#detail-meta').textContent,diagram:!!document.querySelector('#diagram-content svg')})");
 if(!detail.diagram||!detail.meta.includes("ALKANE"))throw Error("Problem detail failed");
 let theme=await evalJs("document.querySelector('#theme-toggle').click();document.body.classList.contains('light')");
 await evalJs("document.querySelector('#theme-toggle').click()");
 if(!theme)throw Error("Theme toggle did not work");
 await send("Emulation.setDeviceMetricsOverride",{width:1440,height:900,deviceScaleFactor:1,mobile:false});
 await sleep(350);let big=await send("Page.captureScreenshot",{format:"png",captureBeyondViewport:false});fs.writeFileSync(path.join(screenshots,"desktop.png"),Buffer.from(big.data,"base64"));
 await send("Emulation.setDeviceMetricsOverride",{width:390,height:844,deviceScaleFactor:1,mobile:true});
 await sleep(650);
 const mobile=await evalJs("({scrollWidth:document.documentElement.scrollWidth,innerWidth:innerWidth,viewport:document.documentElement.clientWidth})");
 let shot=await send("Page.captureScreenshot",{format:"png",captureBeyondViewport:false});fs.writeFileSync(path.join(screenshots,"mobile.png"),Buffer.from(shot.data,"base64"));
 if(mobile.scrollWidth>mobile.innerWidth+2)throw Error("Mobile horizontal overflow "+JSON.stringify(mobile));
 if(errors.length)throw Error("Runtime errors: "+errors.join(" | "));
 console.log("SITE_SMOKE_PASS",JSON.stringify({url:target,summary:{title:summary.title,sections:summary.sections,cards:summary.cards,tabs:summary.tabs,images:summary.images.length},samples:expect,mobile,scriptErrors:errors.length,screenshots}));
}
main().catch(e=>{console.error("SITE_SMOKE_FAIL",e.stack||String(e));process.exitCode=1}).finally(()=>{try{ws?.close()}catch{};try{child.kill()}catch{};setTimeout(()=>{fs.rmSync(profile,{recursive:true,force:true})},800)});
