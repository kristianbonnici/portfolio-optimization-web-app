<h1 align="center">Portfolio Optimizer</h1>

<p align="center">Portfolio optimization web app.</p>

## Live app

You can find a running system to use at [portfolio-optim.herokuapp.com/](https://portfolio-optim.herokuapp.com/).

## Introduction
`portfolio-optimization-web-app` is a web application for generating optimal portfolios based on Sharpe Ratio.


## Screenshots

<p align="center">
  <img src="https://github.com/kristianbonnici/portfolio-optimization-web-app/blob/master/portfoliodash/static/images/Screenshot1.png?raw=true" width="800" />
</p>
<p align="center">
  <img src="https://github.com/kristianbonnici/portfolio-optimization-web-app/blob/master/portfoliodash/static/images/Screenshot2.png?raw=true" width="800" />
</p>

## The architecture

<p align="center">
  <img src="https://github.com/kristianbonnici/portfolio-optimization-web-app/blob/master/portfoliodash/static/images/Portfolio-Optimizer-Architecture.drawio.png?raw=true" width="800" />
</p>

1. The user navigates to the site, feeds input details, and presses the "OPTIMIZE" button.
2. Yahoo Finance API intakes the details and retrieves the requested data.
3. [Optifolio](https://github.com/kristianbonnici/optifolio) intakes the data to optimize the portfolio and display the results on the page.

## Built With

**Back End:**
- **[Flask](https://flask.palletsprojects.com/en/2.0.x/)** - The web application framework used
- **[Python](https://www.python.org/)** - Backend language used
- **[Optifolio [PyPI Package]](https://github.com/kristianbonnici/optifolio)** - My package used for portfolio optimization

**Front End:**
- **HTML** - used to design the front-end portion
- **CSS** - used to style the front-end portion
- **JavaScript** - used to create some interactivity


## Author

**Kristian Bonnici**

- [Profile](https://github.com/kristianbonnici)
- [Email](mailto:kristian.bonnici@aalto.fi)
- [Website](https://kristianbonnici.github.io/)

## 🤝 Support

Contributions, issues, and feature requests are welcome!

Give a ⭐️ if you like this project!
