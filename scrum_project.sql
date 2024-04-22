-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 19, 2024 at 05:30 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `scrum`
--

-- --------------------------------------------------------

--
-- Table structure for table `checklistitems`
--

CREATE TABLE `checklistitems` (
  `ChecklistitemID` int(11) NOT NULL,
  `ChecklistID` int(11) DEFAULT NULL,
  `Description` varchar(1023) DEFAULT NULL,
  `IsCompleted` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `checklistitems`
--

INSERT INTO `checklistitems` (`ChecklistitemID`, `ChecklistID`, `Description`, `IsCompleted`) VALUES
(1, 1, 'inleiding', 1),
(2, 1, 'middenstuk', 0),
(3, 1, 'slot', 0),
(4, 2, 'brainstormsessie', 1),
(5, 2, 'uitvoeren', 1);

-- --------------------------------------------------------

--
-- Table structure for table `checklists`
--

CREATE TABLE `checklists` (
  `ChecklistID` int(11) NOT NULL,
  `TicketID` int(11) DEFAULT NULL,
  `Title` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `checklists`
--

INSERT INTO `checklists` (`ChecklistID`, `TicketID`, `Title`) VALUES
(1, 1, 'checklist opbouw'),
(2, 2, 'code schrijven flask checklist');

-- --------------------------------------------------------

--
-- Table structure for table `rights`
--

CREATE TABLE `rights` (
  `RightID` int(11) NOT NULL,
  `Rightname` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rights`
--

INSERT INTO `rights` (`RightID`, `Rightname`) VALUES
(1, 'Geen rechten'),
(2, 'Eigen tickets verslepen'),
(3, 'Tickets claimen'),
(4, 'Aanpassen eigen tickets'),
(5, 'Tickets toevoegen'),
(6, 'Alle tickets editen en verwijderen');

-- --------------------------------------------------------

--
-- Table structure for table `status`
--

CREATE TABLE `status` (
  `StatusID` int(11) NOT NULL,
  `Statusname` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `status`
--

INSERT INTO `status` (`StatusID`, `Statusname`) VALUES
(1, 'Backlog'),
(2, 'Ready'),
(3, 'In Progress'),
(4, 'Review'),
(5, 'Done');

-- --------------------------------------------------------

--
-- Table structure for table `tickets`
--

CREATE TABLE `tickets` (
  `TicketID` int(11) NOT NULL,
  `Title` varchar(255) DEFAULT NULL,
  `Description` varchar(1023) DEFAULT NULL,
  `Hours` int(11) DEFAULT NULL,
  `StatusID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tickets`
--

INSERT INTO `tickets` (`TicketID`, `Title`, `Description`, `Hours`, `StatusID`) VALUES
(1, 'overleg', 'overleg over Python', 7, 1),
(2, 'code schrijven flask', 'code schrijven flask', 6, 1),
(3, 'wachten op koffie', 'wij gaan niet werken tot er nieuwe koffie is', 1, 3);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `UserID` int(11) NOT NULL,
  `Username` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `RightID` int(11) DEFAULT NULL,
  `profile_picture` blob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`UserID`, `Username`, `Password`, `RightID`, `profile_picture`) VALUES
(1, 'Remco', '01234567', 5, 0x68747470733a2f2f6e6f732e6e6c2f6e69657577737575722f617274696b656c2f323138333437392d6b72696a67742d64657a652d6d616b61616b2d6161702d616c736e6f672d6865742d6175746575727372656368742d6f702d7a696a6e2d73656c666965),
(2, 'Thijs', '87654321', 4, 0x666f746f6a7065672e6a706567),
(3, 'Amr', 'c152246c91ef62f553d2109b68698b19f7dd83328374abc489920bf2e2e23510', 3, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `userticket`
--

CREATE TABLE `userticket` (
  `UserTicketID` int(11) NOT NULL,
  `UserID` int(11) DEFAULT NULL,
  `TicketID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `userticket`
--

INSERT INTO `userticket` (`UserTicketID`, `UserID`, `TicketID`) VALUES
(1, 1, 2),
(2, 2, 1),
(3, 3, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `checklistitems`
--
ALTER TABLE `checklistitems`
  ADD PRIMARY KEY (`ChecklistitemID`),
  ADD KEY `ChecklistID` (`ChecklistID`);

--
-- Indexes for table `checklists`
--
ALTER TABLE `checklists`
  ADD PRIMARY KEY (`ChecklistID`),
  ADD KEY `TicketID` (`TicketID`);

--
-- Indexes for table `rights`
--
ALTER TABLE `rights`
  ADD PRIMARY KEY (`RightID`);

--
-- Indexes for table `status`
--
ALTER TABLE `status`
  ADD PRIMARY KEY (`StatusID`);

--
-- Indexes for table `tickets`
--
ALTER TABLE `tickets`
  ADD PRIMARY KEY (`TicketID`),
  ADD KEY `statusID` (`StatusID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`UserID`),
  ADD KEY `rightID` (`RightID`);

--
-- Indexes for table `userticket`
--
ALTER TABLE `userticket`
  ADD PRIMARY KEY (`UserTicketID`),
  ADD KEY `UserID` (`UserID`),
  ADD KEY `TicketID` (`TicketID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `checklistitems`
--
ALTER TABLE `checklistitems`
  MODIFY `ChecklistitemID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `checklists`
--
ALTER TABLE `checklists`
  MODIFY `ChecklistID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `rights`
--
ALTER TABLE `rights`
  MODIFY `RightID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `status`
--
ALTER TABLE `status`
  MODIFY `StatusID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tickets`
--
ALTER TABLE `tickets`
  MODIFY `TicketID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `userticket`
--
ALTER TABLE `userticket`
  MODIFY `UserTicketID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `checklistitems`
--
ALTER TABLE `checklistitems`
  ADD CONSTRAINT `checklistitems_ibfk_1` FOREIGN KEY (`ChecklistID`) REFERENCES `checklists` (`ChecklistID`);

--
-- Constraints for table `checklists`
--
ALTER TABLE `checklists`
  ADD CONSTRAINT `checklists_ibfk_1` FOREIGN KEY (`TicketID`) REFERENCES `tickets` (`TicketID`);

--
-- Constraints for table `tickets`
--
ALTER TABLE `tickets`
  ADD CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`StatusID`) REFERENCES `status` (`StatusID`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`RightID`) REFERENCES `rights` (`RightID`);

--
-- Constraints for table `userticket`
--
ALTER TABLE `userticket`
  ADD CONSTRAINT `userticket_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`),
  ADD CONSTRAINT `userticket_ibfk_2` FOREIGN KEY (`TicketID`) REFERENCES `tickets` (`TicketID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
