describe('Home Page', () => {
  it('can place and receive order', () => {
    cy.visit('/');

    cy.contains('Order Food').click();
    cy.focused().type('Pizza{enter}');
    cy.contains('Order placed successfully').should('be.visible');
    cy.contains('Table 1').parent().parent().contains('Pending').should('be.visible');
    cy.contains('Table 1').parent().parent().contains('Pizza').should('be.visible')


    cy.contains('Status: Received', {
      timeout: 17500, // max order time + a few seconds
    }).should('be.visible');
  })
})