// Small JS for interactivity: set year and simple project modal
document.addEventListener('DOMContentLoaded',()=>{
  const yearEl=document.getElementById('year');
  if(yearEl) yearEl.textContent=new Date().getFullYear();

  // Simple project card click to show details (sample)
  const cards=document.querySelectorAll('.card');
  cards.forEach(card=>{
    card.addEventListener('click',()=>{
      const title=card.dataset.title||card.querySelector('h3')?.textContent||'Project';
      const desc=card.querySelector('p')?.textContent||'';
      showModal(title,desc);
    });
  });
});
function showModal(title,desc){
  const modal=document.createElement('div');
  modal.className='pd-modal';
  modal.innerHTML=`<div class="pd-modal-backdrop"></div><div class="pd-modal-card"><h3>${escapeHtml(title)}</h3><p>${escapeHtml(desc)}</p><button id="pd-close">Close</button></div>`;
  document.body.appendChild(modal);
  document.getElementById('pd-close').addEventListener('click',()=>modal.remove());
}
function escapeHtml(s){return String(s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);}
// Minimal modal styles injected so the modal works without editing CSS file further
(function inject(){
  const css=`.pd-modal{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;z-index:9999}.pd-modal-backdrop{position:absolute;inset:0;background:rgba(2,6,23,0.7)}.pd-modal-card{position:relative;background:#071024;padding:1.25rem;border-radius:10px;max-width:520px;width:90%;color:#e6eef8;z-index:2} .pd-modal-card button{margin-top:1rem;background:#7c3aed;border:none;padding:0.5rem 0.75rem;border-radius:8px;color:#fff;cursor:pointer}`;
  const s=document.createElement('style');s.textContent=css;document.head.appendChild(s);
})();