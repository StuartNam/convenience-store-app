const tablecontent = document.querySelector("tbody");
let users = [];
let onHoverElement = [];
//Define Helper function
const getData = fetch("https://jsonplaceholder.typicode.com/users")
  .then((data) => {
    return data.json();
  })
  .then((data) => {
    users = data;
  });

const renderItem = (index, user) => {
  const item = document.createElement("tr");
  item.innerHTML = `<th>${index}</th>
  <td>${user.phone}</td>
  <td>${user.address.zipcode}</td>
  <td>${user.username}</td>
  <td></td>`;
  item.classList.add("hover","h-12");
  tablecontent.append(item);
};

//Fetch data
async function didMount() {
  await getData;
  users.map((user, index) => {
    renderItem(index + 1, user);
    console.log(user);
  });
  onHoverElement = document.querySelectorAll(".hover");
  console.log(onHoverElement[1]);
  for (let i = 0; i < users.length; i++) {
    onHoverElement[i].addEventListener("mouseenter", (event) => {
      onHoverElement[i].lastChild.innerHTML = `
      <form action="clerk.html" method = "delete" >
      <button class ="btn btn-error mx-auto btn-sm" >Delete</button>
      </form>`;
    });
    onHoverElement[i].addEventListener("mouseleave", (event) => {
      onHoverElement[i].lastChild.innerHTML = "";
    });
  }
}
didMount();


