describe('Home Page', () => {
  it('can place and receive order', () => {
    cy.visit('/');

    cy.contains('Order Food', {
      timeout: 10_000, // wait for app to load
    }).click();
    cy.focused().type('Pizza{enter}');
    cy.contains('Order placed successfully').should('be.visible');
    cy.contains('Table 1').parent().parent().contains('Pending').should('be.visible');
    cy.contains('Table 1').parent().parent().contains('Pizza').should('be.visible')


    cy.contains('Status: Received', {
      timeout: 20_000, // max order time is 15 sec currently, + a few seconds
    }).should('be.visible');

    cy.contains('Table 2').parent().parent().contains('No orders yet.').should('be.visible');
    cy.contains('Table 3').parent().parent().contains('No orders yet.').should('be.visible');
    cy.contains('Table 4').parent().parent().contains('No orders yet.').should('be.visible');
  })
})