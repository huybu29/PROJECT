document.querySelector('.submit').addEventListener('click',()=>{
  const obj={quanity:1};
  obj.quanity=document.querySelector('.quanity').value
  JSON.stringify(obj);
})