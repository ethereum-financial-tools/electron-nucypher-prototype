
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

const SwarmClient = require("@erebos/swarm-browser")
const swarmClient = new SwarmClient({
  bzz: { url: 'http://127.0.0.1:8500' },
})

*/


/*
  DOM things for convenience
*/

let formula = document.querySelector('#formula')
let test = document.querySelector('#run-test')
let status = document.querySelector('#status')
let aliceResult = document.querySelector('#alice-result')
let bobResult = document.querySelector('#bob-result')

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

// start by running the process

formula.textContent = 'Enter some sample text in order to perform a pyUmbral test.';

setTimeout(
  () => { 
    test.dispatchEvent(new Event('click'))
  }, 100)