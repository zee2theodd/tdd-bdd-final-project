Feature: Product Management
  As a customer
  I want to manage products in the system
  So that I can perform CRUD operations and search for specific products

  Background:
    Given the following products
      | name     | description    | price   | available | category    |
      | Hat      | A red fedora   | 59.95   | True      | CLOTHS      |
      | Shoes    | Blue shoes     | 120.50  | False     | CLOTHS      |
      | Big Mac  | 1/4 lb burger  | 5.99    | True      | FOOD        |
      | Sheets   | Full bed sheets| 87.00   | True      | HOUSEWARES  |

  Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "Big Mac"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "1/4 lb burger" in the "Description" field
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I set the "Description" to "Double cheeseburger"
    And I set the "Price" to "6.99"
    And I press the "Update" button
    Then I should see the message "Success"
    When I press the "Retrieve" button
    Then I should see "Double cheeseburger" in the "Description" field
    And I should see "6.99" in the "Price" field

  Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "Shoes"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Blue shoes" in the "Description" field
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Product has been Deleted!"
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "Shoes" in the results

  Scenario: List all Products
    When I visit the "Home Page"
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results

  Scenario: Search by Category
    When I visit the "Home Page"
    And I press the "Clear" button
    And I select "Food" in the "Category" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Big Mac" in the results
    And I should not see "Hat" in the results
    And I should not see "Shoes" in the results
    And I should not see "Sheets" in the results

  Scenario: Search by Availability
    When I visit the "Home Page"
    And I press the "Clear" button
    And I select "True" in the "Available" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results
    And I should not see "Shoes" in the results

  Scenario: Search by Name
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the "Name" field
    And I should see "A red fedora" in the "Description" field
