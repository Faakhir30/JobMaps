document.addEventListener('DOMContentLoaded',async ()=>{
  document.querySelector('.mainFlex').style.display='none';  
  document.querySelector('.loading-screen').style.display='flex';
  await fetch('/scrape').then(response=>response.json()).then(result=>{console.log(result)
    setTimeout(function() {
      document.querySelector('.mainFlex').style.display='flex';  
      document.querySelector('.loading-screen').style.display='none';
      const titles=['job','firms','cities'];
      titles.forEach(element =>LoadStats(element));
       }, 2000);  
  });
  document.getElementById('title').innerHTML='JobMaps! Right Place to find work';
  document.getElementById('company').innerHTML='Search Your Nearest Jobs';
  document.getElementById('location').style.display=`none`;
  document.getElementById('discription').innerHTML='';
  document.getElementById('linkedIN').innerHTML='Made By Faakhir ©';

  
})

function LoadStats(name){
const circle = document.querySelector(`.circle.${name}`);
const circleFill = document.querySelector(`.circle-fill.${name}`);
let circleValue = document.querySelector(`.circle-value.${name}`);
let currentValue = Number(circleValue);
let finalValue = 100;
fetch('/figures').then(response=>response.json()).then(result=>{
  finalValue=result[name];
})
const duration = 2000; // duration of the animation in milliseconds
const start = performance.now(); // start timestamp

function animate() {
  
  const elapsed = performance.now() - start;
  const progress = Math.min(elapsed / duration, 1); // calculate the progress from 0 to 1
  const newValue = Math.round(progress * finalValue); // calculate the new value based on the progress
  circleValue.textContent = newValue; // update the circle text content
  circleFill.style.clip = `rect(0, ${(70 * progress)}px, 70px, 0)`; // update the clip property of the circle-fill element
  if (progress < 1) {
    requestAnimationFrame(animate); // continue the animation
  }
}

animate(); // start the animation
}

function discription(id){
  fetch(`/discription/${id}`, {
    method: 'POST',
    body: JSON.stringify({
      id:id,
    })
})
.then(response => response.json())
.then(result => {
  document.getElementById('title').innerHTML=`<a href=${result.companyLN}>${result.title +" @ "+result.company}</a>`;
  document.getElementById('company').innerHTML='';
  document.getElementById('location').style.display=`block`;
  document.getElementById('location').innerHTML=result.location;
  document.getElementById('discription').innerHTML="DISCRIPTION: \n"+ `${result.discription} `;
  if (result.link!=='')
    lin=result.link;
  else
    lin=result.applyLN;
  document.getElementById('linkedIN').innerHTML=`<a id='applyBtn' target="_blank" href='${lin}'>Apply</a>`

  })
}