
/*
  zerorpc client to access the pyUmbral functionality through
*/

const zerorpc = require("zerorpc")
let client = new zerorpc.Client()

client.connect("tcp://127.0.0.1:4242")

client.invoke("echo", "zerorpc server ready", (error, res) => {
  if(error || res !== 'zerorpc server ready') {
    console.error(error)
  } else {
    console.log("zerorpc server is ready")
  }
})

/*
  Swarm client
  TODO: enable once dependencies are figured out
  NOTE: requires the Swarm service to be running
*/

const Erebos = require("@erebos/swarm-browser")
let swarmClient = new Erebos.SwarmClient({
  bzz: { url: 'http://127.0.0.1:8500' },
})


/*
  DOM things for convenience
*/

let formula = document.querySelector('#formula')
let test = document.querySelector('#run-test')
let status = document.querySelector('#status')
let aliceResult = document.querySelector('#alice-result')
let bobResult = document.querySelector('#bob-result')
let swarmResult = document.querySelector('#swarm-result')


/*

  set up the UI

*/

test.addEventListener('click', () => {

  status.textContent = '';
  bobResult.textContent = '';
  aliceResult.textContent = '';

  client.invoke("calc", formula.value, (error, resContent) => {
    if(error) {
      console.error(error)
    } else {
      resJson = JSON.parse(resContent)
      status.textContent = resJson.success
      aliceResult.textContent = resJson.alice_cleartext
      bobResult.textContent = resJson.bob_cleartext
    }
  })
})

/* 
  test swarm

  To test via Swarm Gateways:
  https://swarm-gateways.net/bzz:/64542a1fe7fda1d246a559e56ac93d8d1607bbd4e0b7c7252805ae4027c5f16c/

*/

const testSwarm = () => {
  let swarmHash = '64542a1fe7fda1d246a559e56ac93d8d1607bbd4e0b7c7252805ae4027c5f16c'
  
  swarmClient.bzz.download(swarmHash)
      .then(res => res.text())
      .then(swarmContent => {
        //console.log(swarmContent)
        swarmResult.textContent = swarmContent
      })

}


/*

  initialization things

*/

// start by running the process

formula.textContent = 'Enter some sample text in order to perform a pyUmbral test.';

// click on the test button for the user

setTimeout(
  () => { 
    test.dispatchEvent(new Event('click'));
    testSwarm();
  }, 100)


