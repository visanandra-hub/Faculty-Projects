/**
 * Hospital Implant Tracker - DataTables Utilities
 * 
 * This file contains utility functions for DataTables initialization in the application.
 */

/**
 * Initialize a DataTable with default options
 * @param {string} tableId - The ID of the table element
 * @param {Object} options - Additional DataTable options
 */
function initDataTable(tableId, options = {}) {
    const defaultOptions = {
        order: [[0, 'desc']],
        paging: true,
        searching: true,
        responsive: true,
        language: {
            emptyTable: "No data available",
            info: "Showing _START_ to _END_ of _TOTAL_ entries",
            infoEmpty: "Showing 0 to 0 of 0 entries",
            infoFiltered: "(filtered from _MAX_ total entries)",
            lengthMenu: "Show _MENU_ entries",
            search: "Search:",
            zeroRecords: "No matching records found",
            paginate: {
                first: "First",
                last: "Last",
                next: "Next",
                previous: "Previous"
            }
        }
    };
    
    const mergedOptions = { ...defaultOptions, ...options };
    return $(tableId).DataTable(mergedOptions);
}

/**
 * Initialize a DataTable that loads data via AJAX
 * @param {string} tableId - The ID of the table element
 * @param {string} url - The API URL to fetch data from
 * @param {Array} columns - The column definitions
 * @param {Object} options - Additional DataTable options
 */
function initAjaxDataTable(tableId, url, columns, options = {}) {
    const defaultOptions = {
        processing: true,
        serverSide: false, // Set to true for server-side processing
        ajax: {
            url: url,
            dataSrc: 'data'
        },
        columns: columns,
        order: [[0, 'desc']],
        paging: true,
        searching: true,
        responsive: true,
        language: {
            emptyTable: "No data available",
            info: "Showing _START_ to _END_ of _TOTAL_ entries",
            infoEmpty: "Showing 0 to 0 of 0 entries",
            infoFiltered: "(filtered from _MAX_ total entries)",
            lengthMenu: "Show _MENU_ entries",
            search: "Search:",
            zeroRecords: "No matching records found",
            paginate: {
                first: "First",
                last: "Last",
                next: "Next",
                previous: "Previous"
            }
        }
    };
    
    const mergedOptions = { ...defaultOptions, ...options };
    return $(tableId).DataTable(mergedOptions);
}

/**
 * Refresh a DataTable
 * @param {Object} table - The DataTable instance
 */
function refreshDataTable(table) {
    table.ajax.reload();
}

/**
 * Create an action button
 * @param {string} url - The button URL
 * @param {string} icon - The button icon class
 * @param {string} btnClass - The button CSS class
 * @param {string} title - The button title
 * @returns {string} HTML for the button
 */
function createActionButton(url, icon, btnClass, title) {
    return `<a href="${url}" class="btn btn-sm ${btnClass}" title="${title}">
                <i class="fas ${icon}"></i>
            </a>`;
}

/**
 * Format a status badge
 * @param {string} status - The status text
 * @returns {string} HTML for the status badge
 */
function formatStatusBadge(status) {
    let badgeClass = 'bg-secondary';
    
    if (status === 'Active') {
        badgeClass = 'bg-success';
    } else if (status === 'Removed') {
        badgeClass = 'bg-danger';
    } else if (status === 'Replaced') {
        badgeClass = 'bg-warning';
    }
    
    return `<span class="badge rounded-pill ${badgeClass}">${status}</span>`;
}

/**
 * Initialize common DataTables for the application
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize DataTable for implants list if it exists
    if (document.getElementById('implantsTable')) {
        initDataTable('#implantsTable');
    }
    
    // Initialize DataTable for users list if it exists
    if (document.getElementById('userTable')) {
        initDataTable('#userTable');
    }
});
