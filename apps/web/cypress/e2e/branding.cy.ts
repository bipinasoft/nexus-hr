describe("NexusHR brand experience", () => {
  it("renders the landing page and key CTAs", () => {
    cy.visit("/");
    cy.contains("NexusHR").should("be.visible");
    cy.contains("Book an HR architecture walkthrough").should("be.visible");
    cy.contains("Create workspace").click();
    cy.url().should("include", "/create-account");
  });
});
