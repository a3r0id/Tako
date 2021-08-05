window.utcArrayToLocal = (utcArray) => {
    out = []
    for (let i of utcArray){
        out.push(new Date(i).toString())
    }
    return out
}

