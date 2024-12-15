

$(document).ready(function () {

  const access_token = sessionStorage.getItem("access_token")
  if (!access_token) {
    window.localStorage.href = "/home/login/"
  }
  // host
  const host = window.location.origin;
  // Define buttons here
  const $refresh_btn = $("#refresh");
  let counter = 1

  // make api call to get the data
  function datAPI(page) {
    if (!page){
      page = localStorage.getItem('data-api-page')
      if (!page){
        page = 1
      }
    }
    $.ajax({
      url: `${host}/api/v1/data/?page=${page}`,
      type: 'GET',
      contentType: 'application/json',
      headers: { "Authorization": `Bearer ${access_token}` }, // Set the content type
      success: function (data) {
        let curr_page = data?.page;
        let next_page = data?.next_page;
        let prev_page = data?.prev_page;
        res = data.results
        $(".unique-data-show").empty('')
        for (const [tableName, tableData] of Object.entries(res)) {
          // console.log(`Key: ${key}, Value: ${value}`);
          const elem = prepare_accordian_item(tableName, tableData, counter)
          counter += 1
          $(".unique-data-show").append(elem)
        }
        const pagination = prapare_pagination(curr_page, prev_page, next_page)
        $(".unique-data-show").append(pagination)

        const $summaryDiv = $("#summary-row")
        $summaryDiv.empty()
        // Add summary
        prepare_summary($summaryDiv, data?.summary)
      },
      error: function (xhr, status, error) {
        if (xhr.status == 401) {
          alert("Permission denied")
          window.location.href = '/home/'
        }

      }
    });

  }
  // call the data api load funtion when initally called
  datAPI()

  function prepare_accordian_item(tablename, data, counter) {

    const { rows, headers } = prepareTableRow(data, tablename);

    // If there are no rows, return an "empty" table message.
    const tableHtml = rows ? `
      <table class="table" id="${tablename}${counter}">
        <thead class="table-light">
          <tr>
            ${headers}
          </tr>
        </thead>
        <tbody>
          ${rows}
        </tbody>
      </table>
    ` : `
      <div>No data found</div>
    `;

    const elem = `
      <div class="accordion-item${tablename}${counter} border" id=${tablename}${counter}>
        <h2 class="accordion-header">
            <button class="accordion-button collapsed  text-capitalize" type="button" data-bs-toggle="collapse"
                data-bs-target="#flush-collapse${tablename}${counter}" aria-expanded="false" aria-controls="flush-collapse${tablename}${counter}">
                ${tablename}
            </button>
        </h2>
        <div id="flush-collapse${tablename}${counter}" class="accordion-collapse collapse" aria-labelledby="flush-heading${tablename}${counter}" data-bs-parent="#accordionFlushExample">
          <div class="accordion-body">
            ${tableHtml}
          </div>
        </div>
      </div>
    `
    return elem
  }


  function prepareTableRow(data, table_name) {
    let rows = ""; // Initialize rows as an empty string.
    let headers = ""; // Initialize headers as an empty string.

    // Check if data exists and is an array
    if (Array.isArray(data) && data.length > 0) {
      // Dynamically generate headers based on the keys of the first item
      const firstItem = data[0];
      headers = Object.keys(firstItem).map(key => `<th>${key}</th>`).join('');

      // Loop through each item and create a row
      data.forEach(function (item) {
        // Create a row for each item based on its keys
        const row = Object.keys(firstItem).map(key => {
          return `<td>${item[key] !== undefined ? item[key] : 'N/A'}</td>`;
        }).join('');

        rows += `<tr>${row}</tr>`;  // Add the row to the table rows
      });
    } else {
      // If no data is available, show "No data found"
      rows = '<tr><td colspan="5">No data found</td></tr>';
      headers = '';  // Add one header for the message
    }

    return { rows, headers }; // Return both rows and headers
  }

  function prapare_pagination(curr_page, prev_page, next_page) {
    // pagination
    localStorage.setItem("data-api-page", curr_page)
    let page = `<nav aria-label="Page navigation example">
      <ul class="pagination justify-content-end">
        <li class="page-item ${prev_page === null ? 'disabled' : ''}" >
        <a class="page-link" href="#" onclick="navigateToPage(${prev_page})">Previous</a></li>
        <li class="page-item"><a class="page-link" href="#">${curr_page}</a></li>
        <li class="page-item ${next_page === null ? 'disabled' : ''}">
        <a class="page-link" href="#" onclick="navigateToPage(${next_page})">Next</a></li>
      </ul>
    </nav>`

    return page
  }

  function prepare_summary(summaryDiv, resSummary) {
    for (let i = 0; i < resSummary.length; i++) {
      const obj = resSummary[i];  // Access the object at the current index
      let elem = `<div id=${obj.tablename}${obj.count}>
        <div class="uk-card uk-card-default uk-card-hover uk-card-small uk-card-body" id="${obj.tablename}${obj.count}-card">
          <h5 class="uk-heading-line uk-text-center uk-text-capitalize"><span>${obj.tablename}: Summary</span></h4>
          <hr>
            <h6 class="card-subtitle mb-2 text-body-secondary text-capitalize">Total Records: ${obj.count}</h6>

        </div>
      </div >`
        summaryDiv.append(elem)
    }
  };

  window.navigateToPage = function (page) {
    datAPI(page)
  };
});

