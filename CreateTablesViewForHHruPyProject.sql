
-- Скрипт для заполнения предварительно созданной БД (например HH)
-- БД предназначена для анализа данных загруженных с HH.ru с помощью проекта на Python hh_scrapy_3

-- Создаем таблицы

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[t_salary](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[vac_id] [int] NULL,
	[salary] [int] NULL,
	[salary_cur] [nchar](10) NULL,
	[salary_from] [int] NULL,
	[salary_to] [int] NULL,
	[Netto_brutto] [nchar](10) NULL,
 CONSTRAINT [PK_t_salary] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[t_skills](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[vacancy] [int] NULL,
	[skill] [nvarchar](250) NULL,
 CONSTRAINT [PK_t_skills] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[t_vacancies](
	[id] [bigint] NOT NULL,
	[name] [nvarchar](250) NULL,
	[description] [nvarchar](max) NULL,
	[salary] [nchar](50) NULL,
	[alternate_url] [nchar](250) NULL,
	[employer_name] [nchar](250) NULL,
	[employer_id] [int] NULL,
	[created_at] [nchar](50) NULL,
	[created_date] [date] NULL,
	[schedule] [nchar](50) NULL,
	[create_row] [smalldatetime] NULL,
 CONSTRAINT [PK_t_vacancies] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

ALTER TABLE [dbo].[t_vacancies] ADD  CONSTRAINT [DF_t_vacancies_create_row]  DEFAULT (getdate()) FOR [create_row]
GO

SET ANSI_NULLS ON
GO

-- Создаем View

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[v_vacancies]
AS
SELECT        dbo.t_vacancies.id, dbo.t_vacancies.name, dbo.t_vacancies.description, dbo.t_salary.salary_from, dbo.t_salary.salary_to, dbo.t_skills.skill
FROM            dbo.t_skills RIGHT OUTER JOIN
                         dbo.t_vacancies ON dbo.t_skills.vacancy = dbo.t_vacancies.id LEFT OUTER JOIN
                         dbo.t_salary ON dbo.t_vacancies.id = dbo.t_salary.vac_id

GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[v_vacancies_0]
AS
SELECT        dbo.t_vacancies.id, dbo.t_vacancies.name, dbo.t_vacancies.description, COALESCE (dbo.t_salary.salary_from, dbo.t_salary.salary_to) AS salary, dbo.t_vacancies.employer_name, dbo.t_vacancies.alternate_url
FROM            dbo.t_vacancies LEFT OUTER JOIN
                         dbo.t_salary ON dbo.t_vacancies.id = dbo.t_salary.vac_id

GO