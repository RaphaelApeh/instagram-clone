const LikeBtn = document.querySelectorAll("#likeBtn")

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