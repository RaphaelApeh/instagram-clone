const LikeBtn = document.querySelectorAll("#likeBtn")
const saveBtn = document.querySelectorAll("#save-btn")

LikeBtn.forEach(btn=>{
    const url = btn.dataset.slug
    btn.addEventListener("click", function(e){
        fetch(url)
        .then(response=>response.json())
        .then(data=>{
            if (data.added){
                document.querySelectorAll("#likes-count").forEach(text => {
                    text.textContent = `You Liked ${data.count} Likes`
                })
            }else{
                document.querySelectorAll("#likes-count").forEach(text => {
                    text.textContent = `${data.count !== 0 ? data.count: "0"} Likes`
                })
            }
            console.log(data)
        })
        .catch(error=>console.log(error))
    })
})

saveBtn.forEach(btn=>{
    const saveUrl = btn.dataset.url
    btn.addEventListener("click", function(e){
        fetch(saveUrl)
        .then(response=> response.json())
        .then(data=> {
            if (data.added){
                btn.innerHTML = `<svg
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M19.875 2H4.125C3.50625 2 3 2.44939 3 3.00481V22.4648C3 23.0202 3.36563 23.1616 3.82125 22.7728L11.5444 16.1986C11.7244 16.0471 12.0225 16.0471 12.2025 16.1936L20.1731 22.7879C20.6287 23.1666 21 23.0202 21 22.4648V3.00481C21 2.44939 20.4994 2 19.875 2ZM19.3125 20.0209L13.3444 15.0827C12.9281 14.7394 12.405 14.5677 11.8763 14.5677C11.3363 14.5677 10.8019 14.7444 10.3856 15.0979L4.6875 19.9502V3.51479H19.3125V20.0209Z"
                      fill="var(--text-dark)"
                      stroke="var(--text-dark)"
                      stroke-width="0.7"
                    />
                  </svg>`
            }else{
                btn.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bookmark-fill" viewBox="0 0 16 16">
                      <path d="M2 2v13.5a.5.5 0 0 0 .74.439L8 13.069l5.26 2.87A.5.5 0 0 0 14 15.5V2a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2"/>
                </svg>
                `
            }
        })
        .catch(error=> console.log(error))
    })
})