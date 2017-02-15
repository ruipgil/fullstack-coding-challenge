const updateNode = (prop, elm, selector, text) => {
  const target = elm.querySelector(selector)
  if (target) {
    target[prop] = text
  }
}

const update_dom = (data) => {
  const storyNodes = document.querySelectorAll(".story")
  data.forEach((storyData, i) => {
    const storyNode = storyNodes[i]

    console.log(storyNode.querySelector('a'))
    updateNode('innerText', storyNode, ".story-title", storyData.title)
    updateNode('href', storyNode, "a", storyData.link)

    const translationNodes = storyNode.querySelectorAll('.translations li')

    // updates nodes
    Object.keys(storyData.translations).sort().forEach((lang, j) => {
      const translationData = storyData.translations[lang]
      const translationNode = translationNodes[j]

      updateNode('innerText', translationNode, '.language', lang)
      updateNode('innerText', translationNode, '.translation', translationData)
    })
  })
}

const update = () => {
  fetch('/.json')
    .then((response) => response.json())
    .then((data) => update_dom(data))
    .catch((err) => console.error(err))
}

update()
setInterval(update, 10000)
