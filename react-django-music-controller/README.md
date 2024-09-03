# Music Control web app

A collaborative music playing system

---
Requirements
---

- Spotify premium
- Users must be connect to the same network

### Launching app

- Run django server

```
python manage.py runserver
```

- Run react frontend

```

```

---
 Tips
---

### React Lifecycle
Each component in React has a lifecycle which you can monitor and manipulate during its three main phases(Mounting, Updating, and Unmounting)<br><br>
[React Lifecycle](https://www.w3schools.com/react/react_lifecycle.asp#:~:text=Each%20component%20in%20React%20has,Mounting%2C%20Updating%2C%20and%20Unmounting.)
<br>

<em>
<strong>Asynchronous programming
</strong>  is a technique that enables your program to start a potentially long-running task, and then rather than having to wait until that task has finished, to be able to continue to be responsive to other events while the task runs.</em><br>


[Introducing asynchronous JavaScript](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Introducing)

<strong>JDjango JsonResponse
</strong>
<br>
JsonResponse is an HttpResponse subclass that helps to create a JSON-encoded response. Its default Content-Type header is set to application/json. The first parameter, data , should be a dict instance. If the safe parameter is set to False, any object can be passed for serialization; otherwise only dict instances are allowed.
<br>

[Request and response objects¶](https://docs.djangoproject.com/en/4.0/ref/request-response/)<br>
[Django JsonResponse](https://zetcode.com/django/jsonresponse/)<br>
<br>

Authorize against the Spotify API
Using and storing authorization and access tokens<br>
[Authorization guide](https://developer.spotify.com/documentation/general/guides/authorization/)<br>
[Web API](https://developer.spotify.com/documentation/web-api/)<br>
[Web API Quick Start](https://developer.spotify.com/documentation/web-api/quick-start/)<br>
[Dev Dashboard](https://developer.spotify.com/dashboard/applications)<br>
<br>

## Polling

A technique where we check for fresh data over a given interval by periodically making API requests to a server. For example, we can use polling if there is data that changes frequently or we need to wait for the server to transition a given state. 
<br>
### **Application** <br>
A real-world use case for polling would be if we used a third-party authentication provider (such as Firebase or Auth0 ) and need to wait on the result before we proceed. When a user registers, we send the user’s data to the authentication provider from the client. Then on the server, we wait for the response from the authentication provider and then create a user in our database.
<br>
During this whole process, the client must wait through the authentication and the user creation on our server. Since we know this process will either succeed or fail reasonably quickly, we can be comfortable implementing a poll that will make API requests to our server every 1 second until we complete the process of registering and creating a new user.
<br>
Another example when a poll could be useful is if we’re tracking a user’s location on a map. In an app like Uber, we are able to watch our driver approach to pick us up by repeatedly polling for the most recent coordinates. Since this data changes frequently, we’ll set up an interval to poll for the location, ensuring we have up-to-date data.
<br>
### **Implementation**<br>

1. We will write a simple poll function that uses promises to resolve the results from the fetch. I’ll paste the code below and explain how it works.

```

const poll = async ({ fn, validate, interval, maxAttempts }) => {
  let attempts = 0;

  const executePoll = async (resolve, reject) => {
    const result = await fn();
    attempts++;

    if (validate(result)) {
      return resolve(result);
    } else if (maxAttempts && attempts === maxAttempts) {
      return reject(new Error('Exceeded max attempts'));
    } else {
      setTimeout(executePoll, interval, resolve, reject);
    }
  };

  return new Promise(executePoll);
};
```

Our **poll** function is a higher-order function that returns a function, **executePoll**. The **executePoll** function returns a promise and will run recursively until a stopping condition is met. The **poll** function takes 4 variables as arguments:

    * **fn**: This is the function we will execute over a given interval. Typically this will be an API request.
    * **validate**: This is also a function where we define a test to see if the data matches what we want which will end the poll. For example, we can simply test if the data exists or we could check if a nested property of the response has reached a certain state<br>
Ex. validate = user => !!user
<br><br>
Ex. validate = checkout => checkout.status === 'COMPLETE'
<br><br>
    * **interval**: This is the time we want to wait between poll requests. This is entirely determined by the use case in your app, and the higher the importance of having the most up to date information, the shorter the interval will need to be between poll requests.
    * **maxAttempts**: We need the ability to set some reasonable upper bound for the number of poll requests to be able to prevent it from running infinitely.<br><br>
Our **poll** function begins by declaring an **attempts** variable which we form a closure around to track how many times we have polled our API. We then declare the **excutePoll** function which returns a promise. This allows us to continuously call **executePoll** recursively and only **resolve** once we reach a valid value.
<br>
The **executePoll** function is also declared as **async** so we can easily execute our **fn** by using **await**. We then increment our **attempts** once it returns. We call validate on the result from fn, and if it returns true, we resolve the value successfully. If the result is not valid, we check if we have reached our maximum poll attempts and throw an error if so. Otherwise, we setTimeout for the given interval and then call the function recursively to attempt the poll again.


2. The example below is once you can paste into a JavaScript file locally and run it using node. It takes the same poll function we built in the previous section and applies it to a fake API request. It simulates waiting for a user to be created, which in this case will happen after 12 seconds. We poll the mock API every second until it returns a user which then resolves to our chained then function.

```js
const poll = ({ fn, validate, interval, maxAttempts }) => {
  console.log('Start poll...');
  let attempts = 0;

  const executePoll = async (resolve, reject) => {
    console.log('- poll');
    const result = await fn();
    attempts++;

    if (validate(result)) {
      return resolve(result);
    } else if (maxAttempts && attempts === maxAttempts) {
      return reject(new Error('Exceeded max attempts'));
    } else {
      setTimeout(executePoll, interval, resolve, reject);
    }
  };

  return new Promise(executePoll);
};

const simulateServerRequestTime = interval => {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve();
    }, interval);
  });
};

const TIME_FOR_AUTH_PROVIDER = 10000;
const TIME_TO_CREATE_NEW_USER = 2000;

let fakeUser = null;
const createUser = (() => {
  setTimeout(() => {
    fakeUser = {
      id: '123',
      username: 'testuser',
      name: 'Test User',
      createdAt: Date.now(),
    };
  }, TIME_FOR_AUTH_PROVIDER + TIME_TO_CREATE_NEW_USER);
})();

const mockApi = async () => {
  await simulateServerRequestTime(500);
  return fakeUser;
};

const validateUser = user => !!user;
const POLL_INTERVAL = 1000;
const pollForNewUser = poll({
  fn: mockApi,
  validate: validateUser,
  interval: POLL_INTERVAL,
})
  .then(user => console.log(user))
  .catch(err => console.error(err));
```

> A great way to poll APIs is to schedule requests in javascript then wait a certain amount of time (no more than 10-30 seconds) for the server to hold the request to see if the song changes then return the result. If the result is found earlier than 10-30 seconds, the server returns it early. The client sees the request as in progress, and can receive it in the entire window the server has it as long as the request does not time out (exceeds 30+ seconds or so). You can also just simply request the url every few seconds to check, but that uses a lot of system resources.

### Supplimentary Resources(polling and websockets)

[WebSockets tutorial: How to go real-time with Node and React With Use Case Project
](https://www.youtube.com/watch?v=LenNpb5zqGE&ab_channel=LogRocket)<br>
[WebSockets vs Long Polling](https://ably.com/blog/websockets-vs-long-polling#:~:text=Generally%2C%20WebSockets%20will%20be%20the,hops%20between%20servers%20and%20devices.)<br>
[Polling vs SSE vs WebSocket— How to choose the right one](https://codeburst.io/polling-vs-sse-vs-websocket-how-to-choose-the-right-one-1859e4e13bd9)<br>
[Polling vs WebSockets](https://www.cookieshq.co.uk/posts/polling-vs-websockets)<br>
[Short Polling vs Long Polling vs WebSockets - System Design](https://www.youtube.com/watch?v=ZBM28ZPlin8&ab_channel=BeABetterDev)<br>
[HTTP Request vs HTTP Long-Polling vs WebSockets vs Server-Sent Events](https://www.youtube.com/watch?v=k56H0DHqu5Y&ab_channel=AfterAcademy)<br>
[Create a Chat App using React, Django, and Node js](https://www.youtube.com/watch?v=aTEIju81QVE&list=PLo7TNe_pEoMXWMuczlaSDdIt2HgRCwggR&ab_channel=AdefemiGreat)<br>


# TO:DO - intergrate spotify free accounts, fix UI